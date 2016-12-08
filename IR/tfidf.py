import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

# import math
# from textblob import TextBlob as tb
# import IR.PortStemmer

class TfIdf():
    _token_dict = {}
    _stemmer = PorterStemmer()
    _tfs = None

    def stem_tokens(self, tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(self._stemmer.stem(item))
        return stemmed

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        stems = stem_tokens(tokens, self._stemmer)
        return stems

    def index(self, documents):
        for n, document in enumerate(documents):
            document = self._p.stem(document.lower().translate(None, string.punctuation))
            self._token_dict[n] = document

        # this can take some time
        self._tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
        self._tfs = self._tfidf.fit_transform(self._token_dict.values())

    def query(self, query):
        response = self._tfidf.transform([query])
        feature_names = tfidf.get_feature_names()
        for col in response.nonzero()[1]:
            print(feature_names[col], ' - ', response[0, col])


    # _index = {}
    # _vocabulary = set()
    # _p = IR.PortStemmer.PortStemmer()
    #
    # def _tf(self, word, blob):
    #     return math.log(blob.count(word) / len(blob) + 1, 10)
    #
    # def _n_containing(self, word, bloblist):
    #     return sum(1 for blob in bloblist if word in blob)
    #
    # def _idf(self, word, bloblist):
    #     return math.log(len(bloblist) / (1 + self._n_containing(word, bloblist)), 10)
    #
    # def _tfidf(self, word, blob, bloblist):
    #     return self._tf(word, blob) * self._idf(word, bloblist)
    #
    # # [ [], [], [] ]
    # def build_index(self, documents):
    #     # find vocabulary
    #     self._index = {}
    #     for document in documents:
    #         for word in document:
    #             word = str(tb(word).words[0])
    #             if word not in self._index:
    #                 self._index[word] = {}
    #             self._vocabulary.add(word)
    #     # calculate tf-idf
    #     for document_index_id, document in enumerate(documents):
    #         for word in self._vocabulary:
    #             self._index[word][document_index_id] = self._tfidf(word, document, documents)
    #
    # def rank_results(self, query):
    #     #lower and stem the query
    #     query = [self._p.stem(_.lower()) for _ in query]
    #
    #     query_vec = {}
    #     for word in query:
    #         query_vec[word] = query_vec.get(word,0) + 1
    #     query_vec = dict( (word, self._tf(word, )  math.log(query_vec[word], 10) + 1.0) for word in query_vec)


