import string
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from sklearn.datasets import fetch_20newsgroups
import nltk
from nltk.corpus import stopwords

from lda.ldamodel2 import LdaModel

cats = ['comp.windows.x', 'talk.religion.misc']
sw_nltk = stopwords.words('english')
texts=fetch_20newsgroups(subset='train', categories=cats).data

def remove_punct(text):
    text=text.lower()
    text=text.translate(str.maketrans('', '', string.punctuation))
    return text

texts_toks=[remove_punct(t).split() for t in texts]
texts_toks_nostop=[[tok for tok in text_toks if tok not in sw_nltk] for text_toks in texts_toks]

common_dictionary = Dictionary(texts_toks_nostop)
common_corpus = [common_dictionary.doc2bow(text) for text in texts_toks_nostop]
print(len(common_corpus))

lda = LdaModel(common_corpus, num_topics=3, passes=100)
# lda = LdaModel(common_texts, num_topics=3, passes=100)
# print(lda.show_topics())
# print(lda.print_topics())

for topic_id in range(3):
    print(f'topic nr {topic_id}')
    topic_words=lda.get_topic_terms(topic_id)
    for word_weight in topic_words:
        print(common_dictionary[word_weight[0]])
