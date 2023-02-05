import numpy as np
from approx_posterior import make_approx_posterior
from exact_posterior import make_exact_posterior
from util import Plot_contour_pdf


def main():
    # Generate data
    mu_gen = 0.7
    sigma_gen = 1.3
    N_gen = 50
    data = mu_gen + np.random.normal(size=(N_gen,))*sigma_gen
    print(data)

    # Make a plotting object so that we can use equal contour lines
    plot_contour = Plot_contour_pdf(N_gen)

    make_exact_posterior(data, plot_contour)
    make_approx_posterior(data, plot_contour)

    print('Sample mean %5.3f \nSample variance %5.3f' % (np.mean(data), np.var(data)))


if __name__ == "__main__":
    main()