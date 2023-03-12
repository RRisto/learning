Typical Sets
============

Source: https://github.com/joshspeagle/typical_sets

Although typical sets are important in understanding how/why sampling
algorithms (do not) work, they are rarely taught when most astronomers are
introduced to sampling methods such as Markov Chain Monte Carlo (MCMC).
This repository includes an interactive Jupyter Notebook that introduces
the idea of typical sets using some basic examples and illustrates why they
make sampling difficult in higher dimensions. It also details how their
behavior shapes various MCMC algorithms such as (Adaptive)
Metropolis-Hastings, ensemble (particle) sampling, and Hamiltonian Monte
Carlo (HMC). Results are both described theoretically and demonstrated using
numerical simulations.

The notebook has minimal requirements to run outside of some imports
used to establish compatibility between notation in Python 2 and 3. Bare-bones
implementations of all the MCMC samplers are implemented "by hand" in the
notebook to outline basic sampling logic and allow any interested users to
experiment with modifications. Users are encouraged to play around with the
code to help build intuition.

A version of these results were presented in a [talk](https://speakerdeck.com/joshspeagle/typical-sets-what-they-are-and-how-to-hopefully-find-them) during [AstroStat Day](http://hea-www.harvard.edu/AstroStat/AstroStatDay/) at the Harvard-Smithsonian Center for Astrophysics on September 20, 2017.