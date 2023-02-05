import matplotlib
import numpy as np
from scipy.special import gamma as gamma_func
import matplotlib.pyplot as plt
from scipy.stats import norm


def ELBO(k, a, b):
    """
    implements equation 21.98 in Murphy
    :param k: the kappa parameter
    :param a: the a parameter
    :param b: the b parameter
    :return:
    """
    return -0.5*np.log(k) + np.log(gamma_func(a)) - a*np.log(b)


def q_mu_distro(mu_par, k_par):
    """
    implements equation 21.71 in Murphy
    :param mu_par: the mu parameter
    :param k_par: the kappa parameter
    :return:
    """
    def q_mu(mu):
        return norm.pdf(mu, loc=mu_par, scale=np.sqrt(1/k_par))
    return q_mu


def q_lambda_distro(a_par, b_par):
    """
    implements equation 21.73 in Murphy
    :param a_par: the a parameter
    :param b_par: the b parameter
    :return:
    """
    def q_lambda(lam):
        return np.power(b_par, a_par)/gamma_func(a_par)*np.power(lam, a_par-1)*np.exp(-b_par*lam)
    return q_lambda


def q_mean_field_distro(mu_par, k_par, a_par, b_par):
    """
    Combines the approximating distributions for \mu and \lambda
    :param mu_par: the mu parameter
    :param k_par: the kappa parameter
    :param a_par: the a parameter
    :param b_par: the b parameter
    :return:
    """
    q_mu_instance = q_mu_distro(mu_par, k_par)
    q_lambda_instance = q_lambda_distro(a_par, b_par)

    def q_mean_field(mu, sigma2):
        # Be careful, argument is sigma2, not lambda!
        lam = 1/(sigma2+1E-9)  # Prevent numerical error
        return q_mu_instance(mu)*q_lambda_instance(lam)
    return q_mean_field


def normal_inv_chi2_distro(mu_par, k_par, nu_par, sigma2_par):
    """
    calculates the NIX distribution

    usage draws inspiration from eqn 4.223 in Murphy

    mu ~ Normal(mu0, sigma_squared/k0)
    sigma_squared ~ inverse_chi_squared(nu0, sigma_squared0)

    :param mu_par: mu parameter for the normal
    :param k_par: kappa parameter for the scaling of variance in the normal
    :param nu_par: degrees of freedom in the inverse chi2 distro
    :param sigma2_par: scale parameter for the inverse chi2 distro
    :return:
    """
    def normal_inv_chi2(mu, sigma2):
        sigma2 += 1E-9  # prevent division by zero error
        first = np.power(2*np.pi*sigma2/k_par, -1/2.)*np.exp(-k_par/(2*sigma2)*(mu-mu_par)**2)
        second = np.power(sigma2_par*nu_par/2., nu_par/2.)/gamma_func(nu_par/2.)\
                    * np.exp((-nu_par*sigma2_par)/(2*sigma2))/ np.power(sigma2, 1+nu_par/2.)
        return first * second
    return normal_inv_chi2


class Plot_contour_pdf:
    def __init__(self, num_points=0):
        self.levels = None
        self.num_levels = 7
        self.num_points = num_points

    def __call__(self, pdf, num_points_plot=20, basename='posterior', stepname=0):
        X, Y = np.meshgrid(np.linspace(-2, 2, num_points_plot), np.linspace(0, 4, num_points_plot))
        P = pdf(X, Y)

        plt.figure()
        CS = plt.contour(X, Y, P, levels=self.levels)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.xlabel('value for \mu')
        plt.ylabel('value for \sigma^2')
        plt.title('%s at step %i with num_points %i' % (basename, stepname, self.num_points))
        CB = plt.colorbar(CS, shrink=0.8, extend='both')

        plt.savefig('im/%s%03d.png' % (basename, stepname))

        self.update_levels(CS.levels)

    def update_levels(self, levels):
        try:
            min_ = min((np.min(levels), np.min(self.levels)))
            max_ = max((np.max(levels), np.max(self.levels)))
        except TypeError:
            min_, max_ = np.min(levels), np.max(levels)
        self.levels = np.linspace(min_, max_, self.num_levels)
