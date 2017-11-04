import random
from collections import Counter


class CustomLDA(object):
    def __init__(self, documents, nr_topics):
        self.documents = documents
        self.nr_topics = nr_topics
        self.distinct_words = None
        self.count_distinct_words()

        self.D = len(self.documents)
        self.W = len(self.distinct_words)

        self.document_topic_counts = None
        self.count_document_topic()

        self.topic_word_counts = None
        self.count_topic_word()

        self.topic_counts = None
        self.count_topic()

        self.document_lengths = None
        self.get_document_lengths()

        self.document_topics = None
        self.init_document_topics()

        self.init_counts()

        self.nr_iter = None
        self.topic_names = None

    def count_document_topic(self):
        self.document_topic_counts = [Counter() for _ in self.documents]

    def count_topic_word(self):
        self.topic_word_counts = [Counter() for _ in range(self.nr_topics)]

    def sample_from(self, weights):
        """returns i with probability weights[i] / sum(weights)"""
        total = sum(weights)
        rnd = total * random.random()  # uniform between 0 and total
        for i, w in enumerate(weights):
            rnd -= w  # return the smallest i such that
            if rnd <= 0:
                return i  # weights[0] + ... + weights[i] >= rnd

    def count_topic(self):
        self.topic_counts = [0 for _ in range(self.nr_topics)]

    def get_document_lengths(self):
        self.document_lengths = list(map(len, self.documents))

    def count_distinct_words(self):
        self.distinct_words = set(word for document in self.documents for word in document)

    def p_topic_given_document(self, topic, d, alpha=0.1):
        """the fraction of words in document _d_
        that are assigned to _topic_ (plus some smoothing)"""
        return ((self.document_topic_counts[d][topic] + alpha) /
                (self.document_lengths[d] + self.nr_topics * alpha))

    def p_word_given_topic(self, word, topic, beta=0.1):
        """the fraction of words assigned to _topic_
        that equal _word_ (plus some smoothing)"""
        return ((self.topic_word_counts[topic][word] + beta) /
                (self.topic_counts[topic] + self.W * beta))

    def init_document_topics(self):
        random.seed(0)
        self.document_topics = [[random.randrange(self.nr_topics) for word in document] for document in self.documents]

    def init_counts(self):
        for d in range(self.D):
            for word, topic in zip(self.documents[d], self.document_topics[d]):
                self.document_topic_counts[d][topic] += 1
                self.topic_word_counts[topic][word] += 1
                self.topic_counts[topic] += 1

    def topic_weight(self, d, word, k):
        """given a document and a word in that document,
        return the weight for the kth topic"""
        return self.p_word_given_topic(word, k) * self.p_topic_given_document(k, d)

    def choose_new_topic(self, d, word):
        return self.sample_from([self.topic_weight(d, word, k)
                                 for k in range(self.nr_topics)])

    def train(self, nr_iter):
        self.nr_iter = nr_iter
        for iter in range(self.nr_iter):
            for d in range(self.D):
                for i, (word, topic) in enumerate(zip(self.documents[d],
                                                      self.document_topics[d])):
                    # remove this word / topic from the counts
                    # so that it doesn't influence the weights
                    self.document_topic_counts[d][topic] -= 1
                    self.topic_word_counts[topic][word] -= 1
                    self.topic_counts[topic] -= 1
                    self.document_lengths[d] -= 1

                    # choose a new topic based on the weights
                    new_topic = self.choose_new_topic(d, word)
                    self.document_topics[d][i] = new_topic

                    # and now add it back to the counts
                    self.document_topic_counts[d][new_topic] += 1
                    self.topic_word_counts[new_topic][word] += 1
                    self.topic_counts[new_topic] += 1
                    self.document_lengths[d] += 1

    def top_words_per_topic(self):
        for k, word_counts in enumerate(self.topic_word_counts):
            for word, count in word_counts.most_common():
                if count > 0:
                    print(k, word, count)

    def assign_topics(self, topic_names):
        self.topic_names = topic_names
        for document, topic_counts in zip(self.documents, self.document_topic_counts):
            print(document)
            for topic, count in topic_counts.most_common():
                if count > 0:
                    print(self.topic_names[topic], count)
            print()


documents = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]

K=4

lda_model=CustomLDA(documents, 4)

lda_model.train(nr_iter=1000)