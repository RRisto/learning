import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer

class Corpus:
    """
    Class handles a collection of documents and transforms strings into sequences of word indices.
    Documents and word indices are shuffled at random.
    """
    def _expand_word_counts(self, doc_word_counts):
        """
        Expands word counts into sequences of words.
        (e.g. word1 with index 1 and count 3 is transformed into the sequence 1 1 1.
        """
        docs = []
        for doc in doc_word_counts:
            words = []
            for word_idx, count in list(zip(doc.nonzero()[1], doc.data)):
                words += [word_idx] * count
            random.shuffle(words)
            docs.append(words)
        return docs
    
    def __init__(self, docs, max_features=10_000, cv=None, stop_words='english'):
        """
        Creates Corpus instance.
        """
        random.shuffle(docs)
        self._docs = docs
        if cv is None:
            # fit count vectorizer
            self._cv = CountVectorizer(stop_words=stop_words, max_features=max_features)
            self._cv.fit(docs)
        else:
            self._cv = cv
        # get vocabulary and word counts for each document
        self._doc_word_counts = self._cv.transform(docs)
        self._vocab = self._cv.get_feature_names()
        
        # expands word counts into sequences of words
        self._docs = self._expand_word_counts(self._doc_word_counts)
        # count number of words in each document
        self._doc_len = np.array(np.sum(self._doc_word_counts, axis=1)).reshape(-1)

    def get_count_vectorizer(self):
        """
        Returns the CountVectorizer for this corpus.
        """
        return self._cv

    @classmethod
    def from_corpus(cls, docs, corpus):
        """
        Returns new corpus from CountVectorizer of the given corpus. 
        """
        return cls(docs, cv=corpus.get_count_vectorizer())
        
    def __len__(self):
        """
        Returns number of documents in corpus
        """
        return len(self._docs)
        
    def get_doc_len(self):
        """
        Returns number of words for each document.
        """
        return self._doc_len
    
    def get_vocab_len(self):
        """
        Returns number of unique words in vocabulary.
        """
        return len(self._vocab)
    
    def __iter__(self):
        """
        Iterates over all documents and yields word sequences (derived from word counts).
        """
        for doc in self._docs:
            yield doc

    def idx2word(self, idx):
        """
        Returns word for given word index.
        """
        return self._vocab[idx]
