from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary

from lda.ldamodel import LdaModel

common_dictionary = Dictionary(common_texts)
common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]


lda = LdaModel(common_corpus, num_topics=10, passes=100)
