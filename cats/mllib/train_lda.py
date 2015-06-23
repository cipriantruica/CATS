# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
from gensim import corpora, models


class TrainLDA:
    def __init__(self, dbname='TwitterDB' ):
        client = pymongo.MongoClient()
        self.db = client[dbname]

    def trainLDA(self, query={}, num_topics=15, num_words=10, iterations=500):
        try:
            documents = []
            documentsDB = self.db.documents.find(query, {'lemmaText': 1, '_id': 0})
            for document in documentsDB:
                documents.append(document['lemmaText'].split())
            dictionary = corpora.Dictionary(documents)
            corpus = [dictionary.doc2bow(document) for document in documents]
            tfidf = models.TfidfModel(corpus)
            corpus_tfidf = tfidf[corpus]

            lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, iterations=iterations, num_topics=15)
            return lda.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)
        except Exception as e:
            print e

