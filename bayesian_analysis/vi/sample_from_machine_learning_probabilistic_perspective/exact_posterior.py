import numpy as np
from util import normal_inv_chi2_distro


def make_exact_posterior(data, plot):
    # First calculate exact results
    # Our prior parameters
    # mu ~ Normal(mu0, sigma_squared/k0)
    # sigma_squared ~ inverse_chi_squared(nu0, sigma_squared0)
    mu_0 = 0.
    k_0 = 1.
    nu_0 = 1.
    sigma2_0 = 1.

    # Find posterior parameters
    # Equations 4.225-4.229 in Murphy
    x_mean = np.mean(data)
    N = len(data)
    k_N = k_0 + N
    nu_N = nu_0 + N
    mu_N = (k_0 * mu_0 + N * x_mean) / k_N
    sigma2_N = 1/nu_N * (nu_0 * sigma2_0 + np.sum(np.square(data - x_mean)) + N*k_0/k_N*(mu_0-x_mean)**2)

    nix2 = normal_inv_chi2_distro(mu_N, k_N, nu_N, sigma2_N)

    plot(nix2, num_points_plot=50, basename='exact_posterior')

