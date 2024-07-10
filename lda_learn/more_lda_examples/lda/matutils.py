import numpy as np
from scipy.special import psi  # gamma function utils


def dirichlet_expectation(alpha):
    """Expected value of log(theta) where theta is drawn from a Dirichlet distribution.

    Parameters
    ----------
    alpha : numpy.ndarray
        Dirichlet parameter 2d matrix or 1d vector, if 2d - each row is treated as a separate parameter vector.

    Returns
    -------
    numpy.ndarray
        Log of expected values, dimension same as `alpha.ndim`.

    """
    if len(alpha.shape) == 1:
        result = psi(alpha) - psi(np.sum(alpha))
    else:
        result = psi(alpha) - psi(np.sum(alpha, 1))[:, np.newaxis]
    return result.astype(alpha.dtype, copy=False)  # keep the same precision as input

def mean_absolute_difference(a, b):
    """Mean absolute difference between two arrays.

    Parameters
    ----------
    a : numpy.ndarray
        Input 1d array.
    b : numpy.ndarray
        Input 1d array.

    Returns
    -------
    float
        mean(abs(a - b)).

    """
    return np.mean(np.abs(a - b))

def logsumexp(x):
    """Log of sum of exponentials.

    Parameters
    ----------
    x : numpy.ndarray
        Input 2d matrix.

    Returns
    -------
    float
        log of sum of exponentials of elements in `x`.

    Warnings
    --------
    For performance reasons, doesn't support NaNs or 1d, 3d, etc arrays like :func:`scipy.special.logsumexp`.

    """
    x_max = np.max(x)
    x = np.log(np.sum(np.exp(x - x_max)))
    x += x_max

    return x

def argsort(x, topn=None, reverse=False):
    """Efficiently calculate indices of the `topn` smallest elements in array `x`.

    Parameters
    ----------
    x : array_like
        Array to get the smallest element indices from.
    topn : int, optional
        Number of indices of the smallest (greatest) elements to be returned.
        If not given, indices of all elements will be returned in ascending (descending) order.
    reverse : bool, optional
        Return the `topn` greatest elements in descending order,
        instead of smallest elements in ascending order?

    Returns
    -------
    numpy.ndarray
        Array of `topn` indices that sort the array in the requested order.

    """
    x = np.asarray(x)  # unify code path for when `x` is not a np array (list, tuple...)
    if topn is None:
        topn = x.size
    if topn <= 0:
        return []
    if reverse:
        x = -x
    if topn >= x.size or not hasattr(np, 'argpartition'):
        return np.argsort(x)[:topn]
    # np >= 1.8 has a fast partial argsort, use that!
    most_extreme = np.argpartition(x, topn)[:topn]
    return most_extreme.take(np.argsort(x.take(most_extreme)))  # resort topn into order

