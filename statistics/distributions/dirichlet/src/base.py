from scipy.special import gammaln, psi
import numpy as np
import math
import pandas as pd

class LDABase:
    """
    Base Class to fit LDA using Collapsed Gibbs Sampling derived from 
    Griffiths and Steyvers (2004): Finding scientific topics
    """
    def __init__(self, corpus, K, alpha="asymmetric", beta=0.01):
        """
        Create LDABase instance.
        """
        self.corpus = corpus
        self.K = K # number of topics
        self.W = corpus.get_vocab_len() # number of words in vocabulary
        self.D = len(corpus) # number of documents

        # initialize count parameters
        self.topic_word_count = np.zeros((self.K, self.W))
        self.doc_topic_count = np.zeros((self.D, self.K))
        self.doc_word_topic_assignment = [[0] * len(doc) for doc in corpus]
        self.topic_count = np.zeros(K)
        self.doc_len = corpus.get_doc_len()

        self.num_tokens = np.sum(corpus.get_doc_len()) # num tokens in corpus

        # initialize parameters for estimation phi and theta 
        self.theta = np.zeros((self.D, self.K))
        self.phi = np.zeros((self.K, self.W))

        # initialize priors
        if isinstance(alpha, (np.ndarray, list)):
            # set alpha from parameters
            self.alpha = np.array(alpha)
        elif alpha == "asymmetric":
            # asymmetric prior alpha
            self.alpha = np.array([1.0 / (k + np.sqrt(K)) for k in range(K)])
        else:
            # symmetric prior alpha
            self.alpha = np.array([1.0 / K] * K)
        # symmetric prior beta
        self.beta = beta
        
        self.log_likelihood_trace = []
        self.perplexity_trace = []
        self.theta_trace = []
        self.phi_trace = []
        self.marginal_topic_dist_trace = []
        self.training = True

    def _get_topic_word_idx(self, topn=10):
        """
        Returns matrix with word index and shape (K,topn).
        """
        topic_word_idx_sorted = np.argpartition(self.phi, kth=range(-topn, 0), axis=-1)[:,-topn:]
        topic_word_idx_sorted = np.flip(topic_word_idx_sorted, axis=-1)
        return topic_word_idx_sorted

    def get_topics(self, topn=10):
        """
        Returns topn words from all topics as list of words and list of word probabilities.
        """
        topics_words = []
        topics_probs = []
        for topic_idx, topic in enumerate(self._get_topic_word_idx(topn)):
            words = []
            probs = []
            for word_idx in topic:
                word = self.corpus.idx2word(word_idx)
                prob = self.phi[topic_idx, word_idx]
                words.append(word)
                probs.append(prob)
            topics_probs.append(probs)
            topics_words.append(words)
        return topics_words, topics_probs

    def print_topics(self, topn=10):
        """
        Prints topn words from all topics.
        """
        words, probs = self.get_topics(topn)
        print("p(w|t)\tword\n")
        for topic_idx, (words, probs) in enumerate(zip(words, probs)):
            print("Topic #{}".format(topic_idx + 1))
            for word, prob in zip(words, probs):
                output = "{:.3f}\t{}".format(prob, word)
                print(output)
            print()

    def set_inference_mode(self):
        """
        Disable training mode.
        """
        self.training = False

    def set_training_mode(self):
        """
        Enable training mode.
        """
        self.training = True

    def update(self, doc_idx, word_idx, pos, topic_idx, count):
        """
        Increases or decreases all count parameters by given count value (+1 or -1).
        """
        if self.training is True: # should not change during inference
            self.topic_word_count[topic_idx,word_idx] += count
            self.topic_count[topic_idx] += count
        self.doc_topic_count[doc_idx,topic_idx] += count
        self.doc_word_topic_assignment[doc_idx][pos] = topic_idx

    def get_topic_assignment(self, doc_idx, pos):
        """
        Returns current topic assignment of word in document doc_idx at given position.
        """
        return self.doc_word_topic_assignment[doc_idx][pos]

    def get_phi(self):
        """
        Returns per-topic word distribution phi.
        Griffiths and Steyvers (2004): Finding scientific topics
        """
        phi = np.zeros((self.K, self.W))
        beta_sum = self.beta * self.W
        for z in range(self.K):
            for w in range(self.W):
                phi[z,w] = (self.topic_word_count[z,w] + self.beta) / (self.topic_count[z] + beta_sum)
        return phi
    
    def get_theta(self):
        """
        Returns per-document topic distribution theta.
        Griffiths and Steyvers (2004): Finding scientific topics
        """
        theta = np.zeros((self.D, self.K))
        alpha_sum = np.sum(self.alpha)
        for d in range(self.D):
            for z in range(self.K):
                theta[d,z] = (self.doc_topic_count[d,z] + self.alpha[z]) / (self.doc_len[d] + alpha_sum)
        return theta
    
    def full_conditional_distribution(self, doc_idx, word_idx, topic_idx):
        """
        Returns full conditional distribution for given document index, word index and topic index.
        Griffiths and Steyvers (2004): Finding scientific topics
        """
        n_w_t = self.topic_word_count[:,word_idx] # get word topic count for word index
        n_t = self.topic_count # get topic count
        n_d_t = self.doc_topic_count[doc_idx] # get doc topic count for doc index
        n_d = self.doc_len[doc_idx] # get document word count
        
        word_topic_ratio = (n_w_t + self.beta) / (n_t + self.W * self.beta)
        topic_doc_ratio = (n_d_t + self.alpha) / (n_d + np.sum(self.alpha))
        p_z_cond = word_topic_ratio * topic_doc_ratio
        return p_z_cond / p_z_cond.sum()
    
    def get_log_likelihood(self):
        """
        Returns joint log likelihood p(w, z) = p(w|z)p(z).
        Griffiths and Steyvers (2004): Finding scientific topics
        """
        log_likelihood = 0.0
        for z in range(self.K): # log p(w|z)
            log_likelihood += gammaln(self.W * self.beta)
            log_likelihood -= self.W * gammaln(self.beta)
            log_likelihood += np.sum(gammaln(self.topic_word_count[z] + self.beta))
            log_likelihood -= gammaln(np.sum(self.topic_word_count[z] + self.beta))
        for doc_idx, _ in enumerate(self.corpus): # log p(z)
            log_likelihood += gammaln(np.sum(self.alpha))
            log_likelihood -= np.sum(gammaln(self.alpha))
            log_likelihood += np.sum(gammaln(self.doc_topic_count[doc_idx] + self.alpha))
            log_likelihood -= gammaln(np.sum(self.doc_topic_count[doc_idx] + self.alpha))
        return log_likelihood
    
    def trace_metrics(self):
        """
        Traces metrics to ensure convergency.
        """
        log_likelihood = self.get_log_likelihood()
        perplexity = np.exp(-log_likelihood / self.num_tokens)
        marginal_topic_dist = self.topic_word_count.sum(axis=-1) / self.topic_word_count.sum()
        self.log_likelihood_trace.append(log_likelihood)
        self.perplexity_trace.append(perplexity)
        self.marginal_topic_dist_trace.append(marginal_topic_dist)
    
    def trace_params(self):
        """
        Traces estimates of phi and theta.
        """
        self.phi_trace.append(self.get_phi())
        self.theta_trace.append(self.get_theta())
    
    def plot_topic_prior_alpha(self):
        """
        Plots topic prior alpha.
        """
        pd.DataFrame(self.alpha).plot(legend=False, title="Topic Prior alpha", kind="line")
    
    def plot_metrics(self):
        """
        Plots log likelihood and perplexity trace.
        """
        data = zip(self.log_likelihood_trace, self.perplexity_trace)
        df = pd.DataFrame(data, columns=["Log Likelihood", "Perplexity"])
        df.plot(legend=True, title="Convergence Metrics", figsize=(15,5), subplots=True, layout=(1,2))
    
    def plot_marginal_topic_dist(self, topics=None):
        """
        Plots marginal topic distribution trace.
        """
        pd.DataFrame(self.marginal_topic_dist_trace).plot(title="Marginal Topic Distribution", kind="line", figsize=(15, 10))
    
    def plot_doc_theta_trace(self, doc_idx):
        """
        Plots theta trace for given document.
        """
        pd.DataFrame([theta[doc_idx] for theta in self.theta_trace]).plot(title="Doc #{} Topic Distribution".format(doc_idx), kind="line")
