import math
from textblob import TextBlob as tb

class TfIdf():
    _index = {}
    _vocabulary = set()

    def _tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def _n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def _idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def _tfidf(self, word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)

    # [ [], [], [] ]
    def calculate(self, documents):
        # find vocabulary
        self._index = []
        for document in documents:
            self._index[word] = {}
            for word in documents:
                word = tb(word)
                self._vocabulary.add(word)
        # calculate tf-idf
        for document in documents:
            for word in self._vocabulary:
                self._index[word][document] = self._tfidf(word, document, documents)




