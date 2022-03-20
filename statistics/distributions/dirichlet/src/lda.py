from .base import LDABase
from numpy.random import multinomial
from numpy.random import randint
import numpy as np
from scipy.special import gammaln, psi

class LDA(LDABase):
    """
    Class to fit LDA using collapsed Gibbs Sampling derived from 
    Griffiths and Steyvers (2004): Finding scientific topics
    """
    def __init__(self, corpus, K, alpha="asymmetric", beta=0.01, samples=100, burnin=200, interval=2, eval_every=5):
        """
        Create LDA instance.
        """
        super().__init__(corpus=corpus, K=K, alpha=alpha, beta=beta)
        self.burnin = burnin
        self.samples = samples
        self.interval = interval
        self.eval_every = eval_every

    def random_init(self):
        """
        Initializes all LDA variables at random.
        """
        for doc_idx, doc in enumerate(self.corpus):
            for pos, word_idx in enumerate(doc):
                new_topic_idx = randint(self.K)
                self.update(doc_idx, word_idx, pos, new_topic_idx, 1)

    def update_params(self, burnin=None, interval=None):
        """
        Updates parameters phi and theta based on parameters burnin and interval.
        Computes mean over all samples in trace.
        """
        if burnin is not None:
            if burnin > self.samples:
                raise AttributeError("burnin > samples is not allowed.")
            self.burnin = burnin
        if interval is not None:
            self.interval = interval
        self._update_phi()
        self._update_theta()

    def _update_phi(self):
        """
        Updates phi based on parameters burnin and interval. 
        """
        if len(self.phi_trace) == 0:
            return
        phi = [phi for idx, phi in enumerate(self.phi_trace[self.burnin:]) if idx % self.interval == 0]
        self.phi = np.array(phi).mean(axis=0)
    
    def _update_theta(self):
        """
        Updates theta based on parameters burnin and interval.
        """
        if len(self.theta_trace) == 0:
            return
        theta = [theta for idx, theta in enumerate(self.theta_trace[self.burnin:]) if idx % self.interval == 0]
        self.theta = np.array(theta).mean(axis=0)
    
    @classmethod
    def create_instance(cls, corpus, K, **kwargs):
        """
        Create new LDA instance.
        """
        return cls(corpus, K=K, **kwargs)
    
    def _optimize_prior_alpha(self):
        """
        Adjust alpha using Minka's fixed-point iteration. 
        See Minka (2000): Estimating a Dirichlet distribution and 
        https://people.cs.umass.edu/~cxl/cs691bm/lec09.html for details.
        """
        num = 0.0
        denom = 0.0
        for doc_idx, _ in enumerate(self.corpus):
            num += psi(self.doc_topic_count[doc_idx] + self.alpha) - psi(self.alpha)
            denom += psi(np.sum(self.doc_topic_count[doc_idx] + self.alpha)) - psi(np.sum(self.alpha))
        self.alpha *= num / denom
    
    def _optimize_prior_beta(self):
        """
        Adjust beta using Minka's fixed-point iteration.
        See Minka (2000): Estimating a Dirichlet distribution and 
        https://people.cs.umass.edu/~cxl/cs691bm/lec09.html for details.
        """
        num = 0.0
        denom = 0.0
        for z in range(self.K):
            num += np.sum(psi(self.topic_word_count[z] + self.beta) - psi(self.beta))
            denom += psi(np.sum(self.topic_word_count[z] + self.beta)) - psi(self.W * self.beta)
        self.beta = (self.beta * num) / (self.W * denom)

    def _sample(self):
        """
        Samples new topic assignmments for words in all documents and updates current state of posterior.
        """
        for doc_idx, doc in enumerate(self.corpus):
            if doc_idx % 100 == 0:
                print("{} / {}\t\t".format(doc_idx, len(self.corpus)), end="\r")
            for pos, word_idx in enumerate(doc):
                # get topic assignment of current word from document index and position in document
                topic_idx = self.get_topic_assignment(doc_idx, pos)
                # decrement all corpus statistics by one
                self.update(doc_idx, word_idx, pos, topic_idx, -1)
                # compute full conditional posterior
                probs = self.full_conditional_distribution(doc_idx, word_idx, topic_idx)
                # sample new topic assignment for current word
                new_topic_idx = multinomial(1, probs).argmax()
                # increment all corpus statistics by one
                self.update(doc_idx, word_idx, pos, new_topic_idx, 1)

    def fit(self, optimize_priors=True):
        """
        Fits LDA model using collapsed Gibbs Sampling.
        """
        self.random_init()
        for iteration in range(self.burnin + self.samples):
            # 1) generate new samples from chain 
            self._sample()
            # 2) optimize priors alpha and beta if enabled
            if optimize_priors is True:
                self._optimize_prior_alpha()
                self._optimize_prior_beta()

            # trace metrics to ensure convergency
            if iteration % self.eval_every == 0:
                self.trace_metrics()
                # print log likelihood and perplexity
                log_likelihood = self.log_likelihood_trace[-1]
                perplexity = self.perplexity_trace[-1]
                if iteration >= self.burnin:
                    print("sampling iteration %i perplexity %.1f likelihood %.1f" % (iteration, perplexity, log_likelihood))
                else:
                    print("burnin iteration %i perplexity %.1f likelihood %.1f" % (iteration, perplexity, log_likelihood))
            else:
                print("iteration %i" % iteration)
            self.trace_params() # trace lda parameters phi and theta
        self.update_params() # compute mean of phi and theta over selected samples in trace
