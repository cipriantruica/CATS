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
from gensim import corpora, models
import collections
from indexing.vocabulary_index import VocabularyIndex
from mllib.market_matrix import MarketMatrix

if __name__ == '__main__':
    dbname = 'TwitterDB'
    client = pymongo.MongoClient()
    db = client[dbname]

    start = time.time()
    documents = []
    documentsDB = db.documents.find({'gender': 'homme'}, {'lemmaText': 1, '_id': 0})
    for document in documentsDB:
        # print document['lemmaText'].encode('utf8')
        documents.append(document['lemmaText'].split())
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(document) for document in documents]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    topic_model1 = TopicModeling(id2word=dictionary, corpus=corpus_tfidf)
    print 'LDA using lemma text'
    for topic in topic_model1.topicsLDA(num_topics=15, num_iterations=500):
        print topic, '\n'
    end = time.time()

    print 'LDA TF time:', (end - start)

    # just test for the corpus
    # to see where things go wrong when constructing the Matrix Market
    # od = collections.OrderedDict(sorted(dictionary.items()))
    #
    # for key in od:
    #     print key, od[key]
    # print corpus

    vi = VocabularyIndex(dbname=dbname)
    vi.createIndex(query={'gender': 'homme'})

    print 'LDA with Matrix Market'
    start = time.time()
    # entire vocabulary
    mm = MarketMatrix(dbname=dbname)
    mm.build(query=True)

    # without creating the market matrix file
    id2word, id2tweetID, corpus = mm.buildTFIDFMM()

    # for elem in id2word:
    #     print elem, id2word[elem]

    topic_model2 = TopicModeling(id2word=id2word, corpus=corpus)

    for topic in topic_model2.topicsLDA(num_topics=15, num_iterations=500):
        print topic, '\n'
    end = time.time()
    print 'LDA TF time:', (end - start)