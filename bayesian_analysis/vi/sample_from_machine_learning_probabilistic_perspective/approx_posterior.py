import numpy as np
from util import q_mean_field_distro, ELBO


def make_approx_posterior(data, plot):
    # Prior parameters
    # mu ~ Normal(mu0, 1/(lambda*k0))
    # lambda ~ gamma(a0, b0)
    mu_0 = 0.0
    k_0 = 1.0
    a_0 = 1
    b_0 = 1

    # Calculate the posterior parameters
    N = len(data)
    mu_N = (k_0*mu_0 + N*np.mean(data))/(k_0 + N)
    a_N = a_0 + (N+1)/2
    k_N = 1  # Some initial guess

    num_steps = 10
    ELBO_prev = -1E9
    for step in range(num_steps):
        E_mu2 = 1/k_N + np.power(mu_N, 2)
        b_N = b_0 + k_0*(E_mu2 + mu_0**2 - 2*mu_N*mu_0) + 0.5*np.sum(np.power(data, 2) + E_mu2 - 2*mu_N*data)
        k_N = (k_0 + N) * (a_N / b_N)

        # Chech that the ELBO increases monotonically
        ELBO_current = ELBO(k_N, a_N, b_N)
        assert ELBO_current >= ELBO_prev
        ELBO_prev = ELBO_current
        print('ELBO at step %3i/%3i is %8.5f' % (step, num_steps, ELBO_current))

        # Plot
        q_mean_field = q_mean_field_distro(mu_N, k_N, a_N, b_N)
        plot(q_mean_field, num_points_plot=50, basename='approx_posterior', stepname=step)
