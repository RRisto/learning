import itertools
import numbers
import numpy as np


def get_random_state(seed):
    """Generate :class:`numpy.random.RandomState` based on input seed.

    Parameters
    ----------
    seed : {None, int, array_like}
        Seed for random state.

    Returns
    -------
    :class:`numpy.random.RandomState`
        Random state.

    Raises
    ------
    AttributeError
        If seed is not {None, int, array_like}.

    Notes
    -----
    Method originally from `maciejkula/glove-python <https://github.com/maciejkula/glove-python>`_
    and written by `@joshloyal <https://github.com/joshloyal>`_.

    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a np.random.RandomState instance' % seed)


def get_max_id(corpus):
    """Get the highest feature id that appears in the corpus.

    Parameters
    ----------
    corpus : iterable of iterable of (int, numeric)
        Collection of texts in BoW format.

    Returns
    ------
    int
        Highest feature id.

    Notes
    -----
    For empty `corpus` return -1.

    """
    maxid = -1
    for document in corpus:
        if document:
            maxid = max(maxid, max(fieldid for fieldid, _ in document))
    return maxid


class FakeDict:
    """Objects of this class act as dictionaries that map integer->str(integer), for a specified
    range of integers <0, num_terms).

    This is meant to avoid allocating real dictionaries when `num_terms` is huge, which is a waste of memory.

    """

    def __init__(self, num_terms):
        """

        Parameters
        ----------
        num_terms : int
            Number of terms.

        """
        self.num_terms = num_terms

    def __str__(self):
        return "%s<num_terms=%s>" % (self.__class__.__name__, self.num_terms)

    def __getitem__(self, val):
        if 0 <= val < self.num_terms:
            return str(val)
        raise ValueError("internal id out of bounds (%s, expected <0..%s))" % (val, self.num_terms))

    def __contains__(self, val):
        return 0 <= val < self.num_terms

    def iteritems(self):
        """Iterate over all keys and values.

        Yields
        ------
        (int, str)
            Pair of (id, token).

        """
        for i in range(self.num_terms):
            yield i, str(i)

    def keys(self):
        """Override the `dict.keys()`, which is used to determine the maximum internal id of a corpus,
        i.e. the vocabulary dimensionality.

        Returns
        -------
        list of int
            Highest id, packed in list.

        Notes
        -----
        To avoid materializing the whole `range(0, self.num_terms)`,
        this returns the highest id = `[self.num_terms - 1]` only.

        """
        return [self.num_terms - 1]

    def __len__(self):
        return self.num_terms

    def get(self, val, default=None):
        if 0 <= val < self.num_terms:
            return str(val)
        return default


def dict_from_corpus(corpus):
    """Scan corpus for all word ids that appear in it, then construct a mapping
    which maps each `word_id` -> `str(word_id)`.

    Parameters
    ----------
    corpus : iterable of iterable of (int, numeric)
        Collection of texts in BoW format.

    Returns
    ------
    id2word : :class:`~gensim.utils.FakeDict`
        "Fake" mapping which maps each `word_id` -> `str(word_id)`.

    Warnings
    --------
    This function is used whenever *words* need to be displayed (as opposed to just their ids)
    but no `word_id` -> `word` mapping was provided. The resulting mapping only covers words actually
    used in the corpus, up to the highest `word_id` found.

    """
    num_terms = 1 + get_max_id(corpus)
    id2word = FakeDict(num_terms)
    return id2word


def chunkize_serial(iterable, chunksize, as_numpy=False, dtype=np.float32):
    """Yield elements from `iterable` in "chunksize"-ed groups.

    The last returned element may be smaller if the length of collection is not divisible by `chunksize`.

    Parameters
    ----------
    iterable : iterable of object
        An iterable.
    chunksize : int
        Split iterable into chunks of this size.
    as_numpy : bool, optional
        Yield chunks as `np.ndarray` instead of lists.

    Yields
    ------
    list OR np.ndarray
        "chunksize"-ed chunks of elements from `iterable`.

    Examples
    --------
    .. sourcecode:: pycon

        >>> print(list(grouper(range(10), 3)))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    """
    it = iter(iterable)
    while True:
        if as_numpy:
            # convert each document to a 2d numpy array (~6x faster when transmitting
            # chunk data over the wire, in Pyro)
            wrapped_chunk = [[np.array(doc, dtype=dtype) for doc in itertools.islice(it, int(chunksize))]]
        else:
            wrapped_chunk = [list(itertools.islice(it, int(chunksize)))]
        if not wrapped_chunk[0]:
            break
        # memory opt: wrap the chunk and then pop(), to avoid leaving behind a dangling reference
        yield wrapped_chunk.pop()


grouper = chunkize_serial
