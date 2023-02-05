# Variational inference on a normal distribution

This project implements a basic example of variational inference. We infer the posterior mean and variance of sampled real valued numbers. For this model, we also know the exact form for the posterior. Therefore, it helps us to understand how variational inference works. Later, we can use this knowledge for more complicated models.

# What is variational inference?
In variational inference (VI), we approximate a complicated distribution by a simpler approximating distribution. Throughout literature, the true distribution is referred to as <img alt="$p(x)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/c9ea84eb1460d2895e0cf5125bd7f7b5.svg?invert_in_darkmode" align=middle width="30.33723pt" height="24.56552999999997pt"/> and the approximating distribution as <img alt="$q$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width="7.898533500000002pt" height="14.102549999999994pt"/>, we will also use this notation. In our case, the distributions <img alt="$p$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width="8.239720500000002pt" height="14.102549999999994pt"/> and <img alt="$q$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width="7.898533500000002pt" height="14.102549999999994pt"/> represent the posterior over the parameters over our model. In this case, people refer to VI as variational Bayes. 

The distribution <img alt="$q$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width="7.898533500000002pt" height="14.102549999999994pt"/> will approximate <img alt="$p$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width="8.239720500000002pt" height="14.102549999999994pt"/> according to the KL-divergence between the distributions. 

<img alt="$KL(q||p) = \int q(x) log \frac{q(x)}{p(x)} dx$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/b79c7ae8eb0f0202bbe763810e7f5277.svg?invert_in_darkmode" align=middle width="197.65729499999998pt" height="33.14091000000001pt"/>

A high KL divergence means that the distributions are quite different. A low KL divergence means that the distributions look more like eachother. So as we minimize the KL divergence, the distribution <img alt="$q$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width="7.898533500000002pt" height="14.102549999999994pt"/> will approximate <img alt="$p$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width="8.239720500000002pt" height="14.102549999999994pt"/>.

## Reverse KL divergence ?
A natural question follows on why we minimize <img alt="$KL(q||p)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/96488d0599b0a17bc51f40c74de2539e.svg?invert_in_darkmode" align=middle width="64.206615pt" height="24.56552999999997pt"/> and not <img alt="$KL(p||q)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/ec0e9578244feb36319f89e9cb157a53.svg?invert_in_darkmode" align=middle width="64.206615pt" height="24.56552999999997pt"/>? In calculating <img alt="$KL(p||q)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/ec0e9578244feb36319f89e9cb157a53.svg?invert_in_darkmode" align=middle width="64.206615pt" height="24.56552999999997pt"/>, we need samples from <img alt="$p$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width="8.239720500000002pt" height="14.102549999999994pt"/>. However, for the complicated distributions that we want to approximate, it is hard to sample. Either because we have no closed from expression to sample or because the normalization constant is intractable to compute. Therefore, we minimize <img alt="$KL(q||p)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/96488d0599b0a17bc51f40c74de2539e.svg?invert_in_darkmode" align=middle width="64.206615pt" height="24.56552999999997pt"/>. We pick a simple family of distributions, <img alt="$q$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width="7.898533500000002pt" height="14.102549999999994pt"/>, for which we know how to generate samples. [Section 21.2.2 in Murphy](https://mitpress.mit.edu/books/machine-learning-0) has some nice comments on this.

# Our model
We want to infer the posterior over the parameters of a 1D Gaussian. For the precision of the Gaussian, we use a Gamma prior. The model writes down as

<img alt="$p(\mu, \lambda) = \mathcal{N}(\mu| \mu_0, (\kappa \lambda)^{-1})\mathcal{G}amma(\lambda| a_0, b_0)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/033470c5086911efa9bf83d712489467.svg?invert_in_darkmode" align=middle width="307.829445pt" height="26.70657pt"/>

Our approximate posterior for this model will use the mean field approximation. In mean field approximations, we assume that the posterior factorizes over each of the variables. So <img alt="$q(x)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/03fdf3c6a83ab1f3f304bbc20f6cdadf.svg?invert_in_darkmode" align=middle width="29.99832pt" height="24.56552999999997pt"/> is a product of independent <img alt="$q_i(x_i)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/80ad36443385342691c239198bd89ca6.svg?invert_in_darkmode" align=middle width="40.35405pt" height="24.56552999999997pt"/>. Each variable gets its own factor. 

For our model, this implies that we use a separate approximation for <img alt="$\mu$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/07617f9d8fe48b4a7b3f523d6730eef0.svg?invert_in_darkmode" align=middle width="9.867990000000004pt" height="14.102549999999994pt"/> and for <img alt="$\lambda$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/fd8be73b54f5436a5cd2e73ba9b6bfa9.svg?invert_in_darkmode" align=middle width="9.553335pt" height="22.745910000000016pt"/>. Our <img alt="$q$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width="7.898533500000002pt" height="14.102549999999994pt"/> writes as

<img alt="$q(\mu, \lambda) = q(\lambda)q(\mu)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/f16255af098799371b69b6cb02405108.svg?invert_in_darkmode" align=middle width="129.91605pt" height="24.56552999999997pt"/>

# Minimize the KL divergence
Now that we specified our model and approximation, we want to minimize the KL divergence. We assumed that the approximations factorizes over the individual parameters, so our objective is: 

<img alt="$\min_{q(\mu, \lambda)} KL(q||p) \rightarrow \min_{q(\mu), q(\lambda)} KL(q||p)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/6677314bce4547596b54ba292e213282.svg?invert_in_darkmode" align=middle width="305.36269500000003pt" height="24.56552999999997pt"/>

We will minimize this objective with coordinate descent. That means we minimize the objective for one <img alt="$q_i$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/9294da67e8fbc8ee3f1ac635fc79c893.svg?invert_in_darkmode" align=middle width="11.944515000000003pt" height="14.102549999999994pt"/> at a time. When we loop this long enough, we will find a (local) minimum of the objective. In [Murphy, section 25.5.1], this coordinate descent algorithm is derived for our model. Our code implements these equations.

# The lower bound
In our coordinate descent algorithm, we minimize the objective <img alt="$L(q) = KL(q(\mu)q(\lambda)||p(\mu, \lambda))$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/20970731582ddd00f93da36d3213f8ba.svg?invert_in_darkmode" align=middle width="210.104895pt" height="24.56552999999997pt"/>. We can use this quantity to sanity check our implementation. Coordinate descent guarantees us that the objective can only decrease or stay equal at each step. Therefore, we track <img alt="$L$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/ddcb483302ed36a59286424aa5e0be17.svg?invert_in_darkmode" align=middle width="11.145420000000001pt" height="22.381919999999983pt"/> throughout our optimization. If we observe an increase, then we know that our implementation is incorrect.

The value of <img alt="$L(q)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/1cb99bb1bc53bcd42e1e75b24b4c54fa.svg?invert_in_darkmode" align=middle width="31.783785pt" height="24.56552999999997pt"/> has a second function. It turns out that <img alt="$L$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/ddcb483302ed36a59286424aa5e0be17.svg?invert_in_darkmode" align=middle width="11.145420000000001pt" height="22.381919999999983pt"/> is a lower bound on the model evidence. In other words, we know that <img alt="$L(q) = KL(q(\mu)q(\lambda)||p(\mu, \lambda)) \leq log \ p(\mathcal{D}ata)$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/31aa22005eed1eab8fbfd56d0c37cfae.svg?invert_in_darkmode" align=middle width="316.298895pt" height="24.56552999999997pt"/>. As such, we can use the value of <img alt="$L$" src="https://rawgit.com/RobRomijnders/vi_normal/master/svgs/ddcb483302ed36a59286424aa5e0be17.svg?invert_in_darkmode" align=middle width="11.145420000000001pt" height="22.381919999999983pt"/> for model selection.

# Results
Here is a gif of the variational inference with 8 data points. The final image in the gif depicts the exact posterior
![num8](https://github.com/RobRomijnders/vi_normal/blob/master/im/vi_normal_num8.gif?raw=true)

Here is the same procedure with 50 data points
![num50](https://github.com/RobRomijnders/vi_normal/blob/master/im/vi_normal_num50.gif)




# Further reading

  * [Chapter 21 in Murphy on Variational Inference](https://mitpress.mit.edu/books/machine-learning-0)

      * This project draws inspiration from section 21.5.1

  * [Chapter 33 in Mackay on Variational Inference](http://www.inference.org.uk/itprnn/book.pdf)
  * [An intuitive youtube on variational inference by Alex Lamb](https://www.youtube.com/watch?v=h0UE8FzdE8U)
