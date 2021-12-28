import logging
import numbers
import time
from collections import defaultdict

import numpy as np
from scipy.special import psi, polygamma, gammaln

from lda import matutils, utils
from lda.matutils import dirichlet_expectation, mean_absolute_difference, logsumexp
from lda.utils import get_random_state, dict_from_corpus

logger = logging.getLogger(__name__)


def update_dir_prior(prior, N, logphat, rho):
    """Update a given prior using Newton's method, described in
    `J. Huang: "Maximum Likelihood Estimation of Dirichlet Distribution Parameters"
    <http://jonathan-huang.org/research/dirichlet/dirichlet.pdf>`_.

    Parameters
    ----------
    prior : list of float
        The prior for each possible outcome at the previous iteration (to be updated).
    N : int
        Number of observations.
    logphat : list of float
        Log probabilities for the current estimation, also called "observed sufficient statistics".
    rho : float
        Learning rate.

    Returns
    -------
    list of float
        The updated prior.

    """
    gradf = N * (psi(np.sum(prior)) - psi(prior) + logphat)

    c = N * polygamma(1, np.sum(prior))
    q = -N * polygamma(1, prior)

    b = np.sum(gradf / q) / (1 / c + np.sum(1 / q))

    dprior = -(gradf - b) / q

    updated_prior = rho * dprior + prior
    if all(updated_prior > 0):
        prior = updated_prior
    else:
        logger.warning("updated prior is not positive")
    return prior


class LdaState():
    """Encapsulate information for distributed computation of :class:`~gensim.models.ldamodel.LdaModel` objects.

    Objects of this class are sent over the network, so try to keep them lean to
    reduce traffic.

    """

    def __init__(self, eta, shape, dtype=np.float32):
        """

        Parameters
        ----------
        eta : numpy.ndarray
            The prior probabilities assigned to each term.
        shape : tuple of (int, int)
            Shape of the sufficient statistics: (number of topics to be found, number of terms in the vocabulary).
        dtype : type
            Overrides the numpy array default types.

        """
        self.eta = eta.astype(dtype, copy=False)
        self.sstats = np.zeros(shape, dtype=dtype)
        self.numdocs = 0
        self.dtype = dtype

    def reset(self):
        """Prepare the state for a new EM iteration (reset sufficient stats)."""
        self.sstats[:] = 0.0
        self.numdocs = 0

    def merge(self, other):
        """Merge the result of an E step from one node with that of another node (summing up sufficient statistics).

        The merging is trivial and after merging all cluster nodes, we have the
        exact same result as if the computation was run on a single node (no
        approximation).

        Parameters
        ----------
        other : :class:`~gensim.models.ldamodel.LdaState`
            The state object with which the current one will be merged.

        """
        assert other is not None
        self.sstats += other.sstats
        self.numdocs += other.numdocs

    def blend(self, rhot, other, targetsize=None):
        """Merge the current state with another one using a weighted average for the sufficient statistics.

        The number of documents is stretched in both state objects, so that they are of comparable magnitude.
        This procedure corresponds to the stochastic gradient update from
        `'Online Learning for LDA' by Hoffman et al.`_, see equations (5) and (9).

        Parameters
        ----------
        rhot : float
            Weight of the `other` state in the computed average. A value of 0.0 means that `other`
            is completely ignored. A value of 1.0 means `self` is completely ignored.
        other : :class:`~gensim.models.ldamodel.LdaState`
            The state object with which the current one will be merged.
        targetsize : int, optional
            The number of documents to stretch both states to.

        """
        assert other is not None
        if targetsize is None:
            targetsize = self.numdocs

        # stretch the current model's expected n*phi counts to target size
        if self.numdocs == 0 or targetsize == self.numdocs:
            scale = 1.0
        else:
            scale = 1.0 * targetsize / self.numdocs
        self.sstats *= (1.0 - rhot) * scale

        # stretch the incoming n*phi counts to target size
        if other.numdocs == 0 or targetsize == other.numdocs:
            scale = 1.0
        else:
            logger.info("merging changes from %i documents into a model of %i documents", other.numdocs, targetsize)
            scale = 1.0 * targetsize / other.numdocs
        self.sstats += rhot * scale * other.sstats

        self.numdocs = targetsize

    def blend2(self, rhot, other, targetsize=None):
        """Merge the current state with another one using a weighted sum for the sufficient statistics.

        In contrast to :meth:`~gensim.models.ldamodel.LdaState.blend`, the sufficient statistics are not scaled
        prior to aggregation.

        Parameters
        ----------
        rhot : float
            Unused.
        other : :class:`~gensim.models.ldamodel.LdaState`
            The state object with which the current one will be merged.
        targetsize : int, optional
            The number of documents to stretch both states to.

        """
        assert other is not None
        if targetsize is None:
            targetsize = self.numdocs

        # merge the two matrices by summing
        self.sstats += other.sstats
        self.numdocs = targetsize

    def get_lambda(self):
        """Get the parameters of the posterior over the topics, also referred to as "the topics".

        Returns
        -------
        numpy.ndarray
            Parameters of the posterior probability over topics.

        """
        return self.eta + self.sstats

    def get_Elogbeta(self):
        """Get the log (posterior) probabilities for each topic.

        Returns
        -------
        numpy.ndarray
            Posterior probabilities for each topic.
        """
        return dirichlet_expectation(self.get_lambda())

    @classmethod
    def load(cls, fname, *args, **kwargs):
        """Load a previously stored state from disk.

        Overrides :class:`~gensim.utils.SaveLoad.load` by enforcing the `dtype` parameter
        to ensure backwards compatibility.

        Parameters
        ----------
        fname : str
            Path to file that contains the needed object.
        args : object
            Positional parameters to be propagated to class:`~gensim.utils.SaveLoad.load`
        kwargs : object
            Key-word parameters to be propagated to class:`~gensim.utils.SaveLoad.load`

        Returns
        -------
        :class:`~gensim.models.ldamodel.LdaState`
            The state loaded from the given file.

        """
        result = super(LdaState, cls).load(fname, *args, **kwargs)

        # dtype could be absent in old models
        if not hasattr(result, 'dtype'):
            result.dtype = np.float64  # float64 was implicitly used before (because it's the default in numpy)
            logging.info("dtype was not set in saved %s file %s, assuming np.float64", result.__class__.__name__, fname)

        return result


class LdaModel():
    """Train and use Online Latent Dirichlet Allocation model as presented in `'Online Learning for LDA' by Hoffman et al.`_

    Examples
    -------
    Initialize a model using a Gensim corpus

    .. sourcecode:: pycon

        >>> from gensim.test.utils import common_corpus
        >>>
        >>> lda = LdaModel(common_corpus, num_topics=10)

    You can then infer topic distributions on new, unseen documents.

    .. sourcecode:: pycon

        >>> doc_bow = [(1, 0.3), (2, 0.1), (0, 0.09)]
        >>> doc_lda = lda[doc_bow]

    The model can be updated (trained) with new documents.

    .. sourcecode:: pycon

        >>> # In practice (corpus =/= initial training corpus), but we use the same here for simplicity.
        >>> other_corpus = common_corpus
        >>>
        >>> lda.update(other_corpus)

    Model persistency is achieved through :meth:`~gensim.models.ldamodel.LdaModel.load` and
    :meth:`~gensim.models.ldamodel.LdaModel.save` methods.

    """

    def __init__(self, corpus=None, num_topics=100, id2word=None, chunksize=2000, passes=1, update_every=1,
                 alpha='symmetric', eta=None, decay=0.5, offset=1.0, eval_every=10,
                 iterations=50, gamma_threshold=0.001, minimum_probability=0.01,
                 random_state=None, ns_conf=None, minimum_phi_value=0.01,
                 per_word_topics=False, callbacks=None, dtype=np.float32):
        """

        Parameters
        ----------
        corpus : iterable of list of (int, float), optional
            Stream of document vectors or sparse matrix of shape (`num_documents`, `num_terms`).
            If you have a CSC in-memory matrix, you can convert it to a
            streamed corpus with the help of gensim.matutils.Sparse2Corpus.
            If not given, the model is left untrained (presumably because you want to call
            :meth:`~gensim.models.ldamodel.LdaModel.update` manually).
        num_topics : int, optional
            The number of requested latent topics to be extracted from the training corpus.
        id2word : {dict of (int, str), :class:`gensim.corpora.dictionary.Dictionary`}
            Mapping from word IDs to words. It is used to determine the vocabulary size, as well as for
            debugging and topic printing.
        distributed : bool, optional
            Whether distributed computing should be used to accelerate training.
        chunksize :  int, optional
            Number of documents to be used in each training chunk.
        passes : int, optional
            Number of passes through the corpus during training.
        update_every : int, optional
            Number of documents to be iterated through for each update.
            Set to 0 for batch learning, > 1 for online iterative learning.
        alpha : {float, numpy.ndarray of float, list of float, str}, optional
            A-priori belief on document-topic distribution, this can be:
                * scalar for a symmetric prior over document-topic distribution,
                * 1D array of length equal to num_topics to denote an asymmetric user defined prior for each topic.

            Alternatively default prior selecting strategies can be employed by supplying a string:
                * 'symmetric': (default) Uses a fixed symmetric prior of `1.0 / num_topics`,
                * 'asymmetric': Uses a fixed normalized asymmetric prior of `1.0 / (topic_index + sqrt(num_topics))`,
                * 'auto': Learns an asymmetric prior from the corpus (not available if `distributed==True`).
        eta : {float, numpy.ndarray of float, list of float, str}, optional
            A-priori belief on topic-word distribution, this can be:
                * scalar for a symmetric prior over topic-word distribution,
                * 1D array of length equal to num_words to denote an asymmetric user defined prior for each word,
                * matrix of shape (num_topics, num_words) to assign a probability for each word-topic combination.

            Alternatively default prior selecting strategies can be employed by supplying a string:
                * 'symmetric': (default) Uses a fixed symmetric prior of `1.0 / num_topics`,
                * 'auto': Learns an asymmetric prior from the corpus.
        decay : float, optional
            A number between (0.5, 1] to weight what percentage of the previous lambda value is forgotten
            when each new document is examined.
            Corresponds to :math:`\\kappa` from `'Online Learning for LDA' by Hoffman et al.`_
        offset : float, optional
            Hyper-parameter that controls how much we will slow down the first steps the first few iterations.
            Corresponds to :math:`\\tau_0` from `'Online Learning for LDA' by Hoffman et al.`_
        eval_every : int, optional
            Log perplexity is estimated every that many updates. Setting this to one slows down training by ~2x.
        iterations : int, optional
            Maximum number of iterations through the corpus when inferring the topic distribution of a corpus.
        gamma_threshold : float, optional
            Minimum change in the value of the gamma parameters to continue iterating.
        minimum_probability : float, optional
            Topics with a probability lower than this threshold will be filtered out.
        random_state : {np.random.RandomState, int}, optional
            Either a randomState object or a seed to generate one. Useful for reproducibility.
        ns_conf : dict of (str, object), optional
            Key word parameters propagated to :func:`gensim.utils.getNS` to get a Pyro4 nameserver.
            Only used if `distributed` is set to True.
        minimum_phi_value : float, optional
            if `per_word_topics` is True, this represents a lower bound on the term probabilities.
        per_word_topics : bool
            If True, the model also computes a list of topics, sorted in descending order of most likely topics for
            each word, along with their phi values multiplied by the feature length (i.e. word count).
        callbacks : list of :class:`~gensim.models.callbacks.Callback`
            Metric callbacks to log and visualize evaluation metrics of the model during training.
        dtype : {numpy.float16, numpy.float32, numpy.float64}, optional
            Data-type to use during calculations inside model. All inputs are also converted.

        """
        self.dtype = np.finfo(dtype).dtype

        # store user-supplied parameters
        self.id2word = dict_from_corpus(corpus)
        self.num_terms = len(self.id2word)

        # self.distributed = bool(distributed)
        self.num_topics = int(num_topics)
        self.chunksize = chunksize
        self.decay = decay
        self.offset = offset
        self.minimum_probability = minimum_probability
        self.num_updates = 0

        self.passes = passes
        self.update_every = update_every
        self.eval_every = eval_every
        self.minimum_phi_value = minimum_phi_value
        self.per_word_topics = per_word_topics
        # self.callbacks = callbacks

        self.alpha = self.init_dir_prior('alpha')
        self.eta = self.init_dir_prior('eta')

        self.random_state = get_random_state(random_state)

        # VB constants
        self.iterations = iterations
        self.gamma_threshold = gamma_threshold

        self.dispatcher = None
        self.numworkers = 1

        # Initialize the variational distribution q(beta|lambda)
        self.state = LdaState(self.eta, (self.num_topics, self.num_terms), dtype=self.dtype)
        self.state.sstats[...] = self.random_state.gamma(100., 1. / 100., (self.num_topics, self.num_terms))
        self.expElogbeta = np.exp(dirichlet_expectation(self.state.sstats))

        # Check that we haven't accidentally fallen back to np.float64
        assert self.eta.dtype == self.dtype
        assert self.expElogbeta.dtype == self.dtype

        # if a training corpus was provided, start estimating the model right away
        if corpus is not None:
            use_numpy = self.dispatcher is not None
            start = time.time()
            self.update(corpus, chunks_as_numpy=use_numpy)
            # self.add_lifecycle_event(
            #     "created",
            #     msg=f"trained {self} in {time.time() - start:.2f}s",
            # )

    def init_dir_prior(self, name):
        """Initialize priors for the Dirichlet distribution.

        Parameters
        ----------
        prior : {float, numpy.ndarray of float, list of float, str}
            A-priori belief on document-topic distribution. If `name` == 'alpha', then the prior can be:
                * scalar for a symmetric prior over document-topic distribution,
                * 1D array of length equal to num_topics to denote an asymmetric user defined prior for each topic.

            Alternatively default prior selecting strategies can be employed by supplying a string:
                * 'symmetric': (default) Uses a fixed symmetric prior of `1.0 / num_topics`,
                * 'asymmetric': Uses a fixed normalized asymmetric prior of `1.0 / (topic_index + sqrt(num_topics))`,
                * 'auto': Learns an asymmetric prior from the corpus (not available if `distributed==True`).

            A-priori belief on topic-word distribution. If `name` == 'eta' then the prior can be:
                * scalar for a symmetric prior over topic-word distribution,
                * 1D array of length equal to num_words to denote an asymmetric user defined prior for each word,
                * matrix of shape (num_topics, num_words) to assign a probability for each word-topic combination.

            Alternatively default prior selecting strategies can be employed by supplying a string:
                * 'symmetric': (default) Uses a fixed symmetric prior of `1.0 / num_topics`,
                * 'auto': Learns an asymmetric prior from the corpus.
        name : {'alpha', 'eta'}
            Whether the `prior` is parameterized by the alpha vector (1 parameter per topic)
            or by the eta (1 parameter per unique term in the vocabulary).

        Returns
        -------
        init_prior: numpy.ndarray
            Initialized Dirichlet prior:
            If 'alpha' was provided as `name` the shape is (self.num_topics, ).
            If 'eta' was provided as `name` the shape is (len(self.id2word), ).
        is_auto: bool
            Flag that shows if hyperparameter optimization should be used or not.
        """

        if name == 'alpha':
            prior_shape = self.num_topics
        elif name == 'eta':
            prior_shape = self.num_terms
        else:
            raise ValueError("'name' must be 'alpha' or 'eta'")

        init_prior = np.fromiter(
            (1.0 / self.num_topics for i in range(prior_shape)),
            dtype=self.dtype, count=prior_shape,
        )

        return init_prior

    def clear(self):
        """Clear the model's state to free some memory. Used in the distributed implementation."""
        self.state = None
        self.Elogbeta = None

    def sync_state(self, current_Elogbeta=None):
        """Propagate the states topic probabilities to the inner object's attribute.

        Parameters
        ----------
        current_Elogbeta: numpy.ndarray
            Posterior probabilities for each topic, optional.
            If omitted, it will get Elogbeta from state.

        """
        if current_Elogbeta is None:
            current_Elogbeta = self.state.get_Elogbeta()
        self.expElogbeta = np.exp(current_Elogbeta)
        assert self.expElogbeta.dtype == self.dtype

    def inference(self, chunk, collect_sstats=False):
        """Given a chunk of sparse document vectors, estimate gamma (parameters controlling the topic weights)
        for each document in the chunk.

        This function does not modify the model. The whole input chunk of document is assumed to fit in RAM;
        chunking of a large corpus must be done earlier in the pipeline. Avoids computing the `phi` variational
        parameter directly using the optimization presented in
        `Lee, Seung: Algorithms for non-negative matrix factorization"
        <https://papers.nips.cc/paper/1861-algorithms-for-non-negative-matrix-factorization.pdf>`_.

        Parameters
        ----------
        chunk : list of list of (int, float)
            The corpus chunk on which the inference step will be performed.
        collect_sstats : bool, optional
            If set to True, also collect (and return) sufficient statistics needed to update the model's topic-word
            distributions.

        Returns
        -------
        (numpy.ndarray, {numpy.ndarray, None})
            The first element is always returned and it corresponds to the states gamma matrix. The second element is
            only returned if `collect_sstats` == True and corresponds to the sufficient statistics for the M step.

        """
        try:
            len(chunk)
        except TypeError:
            # convert iterators/generators to plain list, so we have len() etc.
            chunk = list(chunk)
        if len(chunk) > 1:
            logger.debug("performing inference on a chunk of %i documents", len(chunk))

        # Initialize the variational distribution q(theta|gamma) for the chunk
        gamma = self.random_state.gamma(100., 1. / 100., (len(chunk), self.num_topics)).astype(self.dtype, copy=False)
        Elogtheta = dirichlet_expectation(gamma)
        expElogtheta = np.exp(Elogtheta)

        assert Elogtheta.dtype == self.dtype
        assert expElogtheta.dtype == self.dtype

        if collect_sstats:
            sstats = np.zeros_like(self.expElogbeta, dtype=self.dtype)
        else:
            sstats = None
        converged = 0

        # Now, for each document d update that document's gamma and phi
        # Inference code copied from Hoffman's `onlineldavb.py` (esp. the
        # Lee&Seung trick which speeds things up by an order of magnitude, compared
        # to Blei's original LDA-C code, cool!).
        integer_types = (int, np.integer,)
        epsilon = np.finfo(self.dtype).eps
        for d, doc in enumerate(chunk):
            if len(doc) > 0 and not isinstance(doc[0][0], integer_types):
                # make sure the term IDs are ints, otherwise np will get upset
                ids = [int(idx) for idx, _ in doc]
            else:
                ids = [idx for idx, _ in doc]
            cts = np.fromiter((cnt for _, cnt in doc), dtype=self.dtype, count=len(doc))
            gammad = gamma[d, :]
            Elogthetad = Elogtheta[d, :]
            expElogthetad = expElogtheta[d, :]
            expElogbetad = self.expElogbeta[:, ids]

            # The optimal phi_{dwk} is proportional to expElogthetad_k * expElogbetad_kw.
            # phinorm is the normalizer.
            # TODO treat zeros explicitly, instead of adding epsilon?
            phinorm = np.dot(expElogthetad, expElogbetad) + epsilon

            # Iterate between gamma and phi until convergence
            for _ in range(self.iterations):
                lastgamma = gammad
                # We represent phi implicitly to save memory and time.
                # Substituting the value of the optimal phi back into
                # the update for gamma gives this update. Cf. Lee&Seung 2001.
                gammad = self.alpha + expElogthetad * np.dot(cts / phinorm, expElogbetad.T)
                Elogthetad = dirichlet_expectation(gammad)
                expElogthetad = np.exp(Elogthetad)
                phinorm = np.dot(expElogthetad, expElogbetad) + epsilon
                # If gamma hasn't changed much, we're done.
                meanchange = mean_absolute_difference(gammad, lastgamma)
                if meanchange < self.gamma_threshold:
                    converged += 1
                    break
            gamma[d, :] = gammad
            assert gammad.dtype == self.dtype
            if collect_sstats:
                # Contribution of document d to the expected sufficient
                # statistics for the M step.
                sstats[:, ids] += np.outer(expElogthetad.T, cts / phinorm)

        if len(chunk) > 1:
            logger.debug("%i/%i documents converged within %i iterations", converged, len(chunk), self.iterations)

        if collect_sstats:
            # This step finishes computing the sufficient statistics for the
            # M step, so that
            # sstats[k, w] = \sum_d n_{dw} * phi_{dwk}
            # = \sum_d n_{dw} * exp{Elogtheta_{dk} + Elogbeta_{kw}} / phinorm_{dw}.
            sstats *= self.expElogbeta
            assert sstats.dtype == self.dtype

        assert gamma.dtype == self.dtype
        return gamma, sstats

    def do_estep(self, chunk, state=None):
        """Perform inference on a chunk of documents, and accumulate the collected sufficient statistics.

        Parameters
        ----------
        chunk : list of list of (int, float)
            The corpus chunk on which the inference step will be performed.
        state : :class:`~gensim.models.ldamodel.LdaState`, optional
            The state to be updated with the newly accumulated sufficient statistics. If none, the models
            `self.state` is updated.

        Returns
        -------
        numpy.ndarray
            Gamma parameters controlling the topic weights, shape (`len(chunk)`, `self.num_topics`).

        """
        if state is None:
            state = self.state
        gamma, sstats = self.inference(chunk, collect_sstats=True)
        state.sstats += sstats
        state.numdocs += gamma.shape[0]  # avoids calling len(chunk) on a generator
        assert gamma.dtype == self.dtype
        return gamma

    def update_alpha(self, gammat, rho):
        """Update parameters for the Dirichlet prior on the per-document topic weights.

        Parameters
        ----------
        gammat : numpy.ndarray
            Previous topic weight parameters.
        rho : float
            Learning rate.

        Returns
        -------
        numpy.ndarray
            Sequence of alpha parameters.

        """
        N = float(len(gammat))
        logphat = sum(dirichlet_expectation(gamma) for gamma in gammat) / N
        assert logphat.dtype == self.dtype

        self.alpha = update_dir_prior(self.alpha, N, logphat, rho)
        logger.info("optimized alpha %s", list(self.alpha))

        assert self.alpha.dtype == self.dtype
        return self.alpha

    def update_eta(self, lambdat, rho):
        """Update parameters for the Dirichlet prior on the per-topic word weights.

        Parameters
        ----------
        lambdat : numpy.ndarray
            Previous lambda parameters.
        rho : float
            Learning rate.

        Returns
        -------
        numpy.ndarray
            The updated eta parameters.

        """
        N = float(lambdat.shape[0])
        logphat = (sum(dirichlet_expectation(lambda_) for lambda_ in lambdat) / N).reshape((self.num_terms,))
        assert logphat.dtype == self.dtype

        self.eta = update_dir_prior(self.eta, N, logphat, rho)

        assert self.eta.dtype == self.dtype
        return self.eta

    def update(self, corpus, chunksize=None, decay=None, offset=None,
               passes=None, update_every=None, eval_every=None, iterations=None,
               gamma_threshold=None, chunks_as_numpy=False):
        """Train the model with new documents, by EM-iterating over the corpus until the topics converge, or until
        the maximum number of allowed iterations is reached. `corpus` must be an iterable.

        In distributed mode, the E step is distributed over a cluster of machines.

        Notes
        -----
        This update also supports updating an already trained model (`self`) with new documents from `corpus`;
        the two models are then merged in proportion to the number of old vs. new documents.
        This feature is still experimental for non-stationary input streams.

        For stationary input (no topic drift in new documents), on the other hand,
        this equals the online update of `'Online Learning for LDA' by Hoffman et al.`_
        and is guaranteed to converge for any `decay` in (0.5, 1].
        Additionally, for smaller corpus sizes,
        an increasing `offset` may be beneficial (see Table 1 in the same paper).

        Parameters
        ----------
        corpus : iterable of list of (int, float), optional
            Stream of document vectors or sparse matrix of shape (`num_documents`, `num_terms`) used to update the
            model.
        chunksize :  int, optional
            Number of documents to be used in each training chunk.
        decay : float, optional
            A number between (0.5, 1] to weight what percentage of the previous lambda value is forgotten
            when each new document is examined. Corresponds to :math:`\\kappa` from
            `'Online Learning for LDA' by Hoffman et al.`_
        offset : float, optional
            Hyper-parameter that controls how much we will slow down the first steps the first few iterations.
            Corresponds to :math:`\\tau_0` from `'Online Learning for LDA' by Hoffman et al.`_
        passes : int, optional
            Number of passes through the corpus during training.
        update_every : int, optional
            Number of documents to be iterated through for each update.
            Set to 0 for batch learning, > 1 for online iterative learning.
        eval_every : int, optional
            Log perplexity is estimated every that many updates. Setting this to one slows down training by ~2x.
        iterations : int, optional
            Maximum number of iterations through the corpus when inferring the topic distribution of a corpus.
        gamma_threshold : float, optional
            Minimum change in the value of the gamma parameters to continue iterating.
        chunks_as_numpy : bool, optional
            Whether each chunk passed to the inference step should be a numpy.ndarray or not. Numpy can in some settings
            turn the term IDs into floats, these will be converted back into integers in inference, which incurs a
            performance hit. For distributed computing it may be desirable to keep the chunks as `numpy.ndarray`.

        """
        # use parameters given in constructor, unless user explicitly overrode them
        if decay is None:
            decay = self.decay
        if offset is None:
            offset = self.offset
        if passes is None:
            passes = self.passes
        if update_every is None:
            update_every = self.update_every
        if eval_every is None:
            eval_every = self.eval_every
        if iterations is None:
            iterations = self.iterations
        if gamma_threshold is None:
            gamma_threshold = self.gamma_threshold

        try:
            lencorpus = len(corpus)
        except Exception:
            logger.warning("input corpus stream has no len(); counting documents")
            lencorpus = sum(1 for _ in corpus)
        if lencorpus == 0:
            logger.warning("LdaModel.update() called with an empty corpus")
            return

        if chunksize is None:
            chunksize = min(lencorpus, self.chunksize)

        self.state.numdocs += lencorpus

        if update_every:
            updatetype = "online"
            if passes == 1:
                updatetype += " (single-pass)"
            else:
                updatetype += " (multi-pass)"
            updateafter = min(lencorpus, update_every * self.numworkers * chunksize)
        else:
            updatetype = "batch"
            updateafter = lencorpus
        evalafter = min(lencorpus, (eval_every or 0) * self.numworkers * chunksize)

        updates_per_pass = max(1, lencorpus / updateafter)
        logger.info(
            "running %s LDA training, %s topics, %i passes over "
            "the supplied corpus of %i documents, updating model once "
            "every %i documents, evaluating perplexity every %i documents, "
            "iterating %ix with a convergence threshold of %f",
            updatetype, self.num_topics, passes, lencorpus,
            updateafter, evalafter, iterations,
            gamma_threshold
        )

        if updates_per_pass * passes < 10:
            logger.warning(
                "too few updates, training might not converge; "
                "consider increasing the number of passes or iterations to improve accuracy"
            )

        # rho is the "speed" of updating; TODO try other fncs
        # pass_ + num_updates handles increasing the starting t for each pass,
        # while allowing it to "reset" on the first pass of each update
        def rho():
            return pow(offset + pass_ + (self.num_updates / chunksize), -decay)

        for pass_ in range(passes):
            if self.dispatcher:
                logger.info('initializing %s workers', self.numworkers)
                self.dispatcher.reset(self.state)
            else:
                other = LdaState(self.eta, self.state.sstats.shape, self.dtype)
            dirty = False

            reallen = 0
            chunks = utils.grouper(corpus, chunksize, as_numpy=chunks_as_numpy, dtype=self.dtype)
            for chunk_no, chunk in enumerate(chunks):
                reallen += len(chunk)  # keep track of how many documents we've processed so far

                if eval_every and ((reallen == lencorpus) or ((chunk_no + 1) % (eval_every * self.numworkers) == 0)):
                    self.log_perplexity(chunk, total_docs=lencorpus)

                if self.dispatcher:
                    # add the chunk to dispatcher's job queue, so workers can munch on it
                    logger.info(
                        "PROGRESS: pass %i, dispatching documents up to #%i/%i",
                        pass_, chunk_no * chunksize + len(chunk), lencorpus
                    )
                    # this will eventually block until some jobs finish, because the queue has a small finite length
                    self.dispatcher.putjob(chunk)
                else:
                    logger.info(
                        "PROGRESS: pass %i, at document #%i/%i",
                        pass_, chunk_no * chunksize + len(chunk), lencorpus
                    )
                    gammat = self.do_estep(chunk, other)

                dirty = True
                del chunk

                # perform an M step. determine when based on update_every, don't do this after every chunk
                if update_every and (chunk_no + 1) % (update_every * self.numworkers) == 0:
                    if self.dispatcher:
                        # distributed mode: wait for all workers to finish
                        logger.info("reached the end of input; now waiting for all remaining jobs to finish")
                        other = self.dispatcher.getstate()
                    self.do_mstep(rho(), other, pass_ > 0)
                    del other  # frees up memory

                    if self.dispatcher:
                        logger.info('initializing workers')
                        self.dispatcher.reset(self.state)
                    else:
                        other = LdaState(self.eta, self.state.sstats.shape, self.dtype)
                    dirty = False

            if reallen != lencorpus:
                raise RuntimeError("input corpus size changed during training (don't use generators as input)")

            # # append current epoch's metric values
            # if self.callbacks:
            #     current_metrics = callback.on_epoch_end(pass_)
            #     for metric, value in current_metrics.items():
            #         self.metrics[metric].append(value)

            if dirty:
                # finish any remaining updates
                if self.dispatcher:
                    # distributed mode: wait for all workers to finish
                    logger.info("reached the end of input; now waiting for all remaining jobs to finish")
                    other = self.dispatcher.getstate()
                self.do_mstep(rho(), other, pass_ > 0)
                del other
                dirty = False

    def do_mstep(self, rho, other, extra_pass=False):
        """Maximization step: use linear interpolation between the existing topics and
        collected sufficient statistics in `other` to update the topics.

        Parameters
        ----------
        rho : float
            Learning rate.
        other : :class:`~gensim.models.ldamodel.LdaModel`
            The model whose sufficient statistics will be used to update the topics.
        extra_pass : bool, optional
            Whether this step required an additional pass over the corpus.

        """
        logger.debug("updating topics")
        # update self with the new blend; also keep track of how much did
        # the topics change through this update, to assess convergence
        previous_Elogbeta = self.state.get_Elogbeta()
        self.state.blend(rho, other)

        current_Elogbeta = self.state.get_Elogbeta()
        self.sync_state(current_Elogbeta)

        # print out some debug info at the end of each EM iteration
        # self.print_topics(5)
        self.show_topics(num_topics=5, num_words=20, log=True)
        diff = mean_absolute_difference(previous_Elogbeta.ravel(), current_Elogbeta.ravel())
        logger.info("topic diff=%f, rho=%f", diff, rho)

        # if self.optimize_eta:
        #     self.update_eta(self.state.get_lambda(), rho)

        if not extra_pass:
            # only update if this isn't an additional pass
            self.num_updates += other.numdocs

    def bound(self, corpus, gamma=None, subsample_ratio=1.0):
        """Estimate the variational bound of documents from the corpus as E_q[log p(corpus)] - E_q[log q(corpus)].

        Parameters
        ----------
        corpus : iterable of list of (int, float), optional
            Stream of document vectors or sparse matrix of shape (`num_documents`, `num_terms`) used to estimate the
            variational bounds.
        gamma : numpy.ndarray, optional
            Topic weight variational parameters for each document. If not supplied, it will be inferred from the model.
        subsample_ratio : float, optional
            Percentage of the whole corpus represented by the passed `corpus` argument (in case this was a sample).
            Set to 1.0 if the whole corpus was passed.This is used as a multiplicative factor to scale the likelihood
            appropriately.

        Returns
        -------
        numpy.ndarray
            The variational bound score calculated for each document.

        """
        score = 0.0
        _lambda = self.state.get_lambda()
        Elogbeta = dirichlet_expectation(_lambda)

        for d, doc in enumerate(corpus):  # stream the input doc-by-doc, in case it's too large to fit in RAM
            if d % self.chunksize == 0:
                logger.debug("bound: at document #%i", d)
            if gamma is None:
                gammad, _ = self.inference([doc])
            else:
                gammad = gamma[d]
            Elogthetad = dirichlet_expectation(gammad)

            assert gammad.dtype == self.dtype
            assert Elogthetad.dtype == self.dtype

            # E[log p(doc | theta, beta)]
            score += sum(cnt * logsumexp(Elogthetad + Elogbeta[:, int(id)]) for id, cnt in doc)

            # E[log p(theta | alpha) - log q(theta | gamma)]; assumes alpha is a vector
            score += np.sum((self.alpha - gammad) * Elogthetad)
            score += np.sum(gammaln(gammad) - gammaln(self.alpha))
            score += gammaln(np.sum(self.alpha)) - gammaln(np.sum(gammad))

        # Compensate likelihood for when `corpus` above is only a sample of the whole corpus. This ensures
        # that the likelihood is always roughly on the same scale.
        score *= subsample_ratio

        # E[log p(beta | eta) - log q (beta | lambda)]; assumes eta is a scalar
        score += np.sum((self.eta - _lambda) * Elogbeta)
        score += np.sum(gammaln(_lambda) - gammaln(self.eta))

        if np.ndim(self.eta) == 0:
            sum_eta = self.eta * self.num_terms
        else:
            sum_eta = np.sum(self.eta)

        score += np.sum(gammaln(sum_eta) - gammaln(np.sum(_lambda, 1)))

        return score

    def show_topics(self, num_topics=10, num_words=10, log=False, formatted=True):
        """Get a representation for selected topics.

        Parameters
        ----------
        num_topics : int, optional
            Number of topics to be returned. Unlike LSA, there is no natural ordering between the topics in LDA.
            The returned topics subset of all topics is therefore arbitrary and may change between two LDA
            training runs.
        num_words : int, optional
            Number of words to be presented for each topic. These will be the most relevant words (assigned the highest
            probability for each topic).
        log : bool, optional
            Whether the output is also logged, besides being returned.
        formatted : bool, optional
            Whether the topic representations should be formatted as strings. If False, they are returned as
            2 tuples of (word, probability).

        Returns
        -------
        list of {str, tuple of (str, float)}
            a list of topics, each represented either as a string (when `formatted` == True) or word-probability
            pairs.

        """
        if num_topics < 0 or num_topics >= self.num_topics:
            num_topics = self.num_topics
            chosen_topics = range(num_topics)
        else:
            num_topics = min(num_topics, self.num_topics)

            # add a little random jitter, to randomize results around the same alpha
            sort_alpha = self.alpha + 0.0001 * self.random_state.rand(len(self.alpha))
            # random_state.rand returns float64, but converting back to dtype won't speed up anything

            sorted_topics = list(matutils.argsort(sort_alpha))
            chosen_topics = sorted_topics[:num_topics // 2] + sorted_topics[-num_topics // 2:]

        shown = []

        topic = self.state.get_lambda()
        for i in chosen_topics:
            topic_ = topic[i]
            topic_ = topic_ / topic_.sum()  # normalize to probability distribution
            bestn = matutils.argsort(topic_, num_words, reverse=True)
            topic_ = [(self.id2word[id], topic_[id]) for id in bestn]
            if formatted:
                topic_ = ' + '.join('%.3f*"%s"' % (v, k) for k, v in topic_)

            shown.append((i, topic_))
            if log:
                logger.info("topic #%i (%.3f): %s", i, self.alpha[i], topic_)

        return shown

    def log_perplexity(self, chunk, total_docs=None):
        """Calculate and return per-word likelihood bound, using a chunk of documents as evaluation corpus.

        Also output the calculated statistics, including the perplexity=2^(-bound), to log at INFO level.

        Parameters
        ----------
        chunk : list of list of (int, float)
            The corpus chunk on which the inference step will be performed.
        total_docs : int, optional
            Number of docs used for evaluation of the perplexity.

        Returns
        -------
        numpy.ndarray
            The variational bound score calculated for each word.

        """
        if total_docs is None:
            total_docs = len(chunk)
        corpus_words = sum(cnt for document in chunk for _, cnt in document)
        subsample_ratio = 1.0 * total_docs / len(chunk)
        perwordbound = self.bound(chunk, subsample_ratio=subsample_ratio) / (subsample_ratio * corpus_words)
        logger.info(
            "%.3f per-word bound, %.1f perplexity estimate based on a held-out corpus of %i documents with %i words",
            perwordbound, np.exp2(-perwordbound), len(chunk), corpus_words
        )
        return perwordbound

    def get_topic_terms(self, topicid, topn=10):
        """Get the representation for a single topic. Words the integer IDs, in constrast to
        :meth:`~gensim.models.ldamodel.LdaModel.show_topic` that represents words by the actual strings.

        Parameters
        ----------
        topicid : int
            The ID of the topic to be returned
        topn : int, optional
            Number of the most significant words that are associated with the topic.

        Returns
        -------
        list of (int, float)
            Word ID - probability pairs for the most relevant words generated by the topic.

        """
        topic = self.get_topics()[topicid]
        topic = topic / topic.sum()  # normalize to probability distribution
        bestn = matutils.argsort(topic, topn, reverse=True)
        return [(idx, topic[idx]) for idx in bestn]

    def get_topics(self):
        """Get the term-topic matrix learned during inference.


        Returns
        -------
        numpy.ndarray
            The probability for each word in each topic, shape (`num_topics`, `vocabulary_size`).

        """
        topics = self.state.get_lambda()
        return topics / topics.sum(axis=1)[:, None]