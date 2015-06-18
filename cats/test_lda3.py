# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.com"
__status__ = "Production"

from mllib.topic_modeling import TopicModeling
import time
import pymongo
from gensim import corpora


if __name__ == '__main__':
    start = time.time()
    dbname = 'TwitterDB'
    client = pymongo.MongoClient()
    db = client[dbname]

    documents = []
    documentsDB =  db.documents.find({'gender': 'homme'}, {'lemmaText': 1, '_id': 0})
    for document in documentsDB:
        documents.append(document['lemmaText'].split())
    id2word = corpora.Dictionary(documents)
    corpus = [id2word.doc2bow(document) for document in documents]

    end = time.time()

    print 'Corpus build:', (end - start)
    start = time.time()
    topic_model = TopicModeling(id2word=id2word, corpus=corpus)
    print 'LDA'
    for topic in topic_model.topicsLDA(num_topics=15):
        print topic, '\n'
    end = time.time()

    print 'LDA TF time:', (end - start)
