# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.com"
__status__ = "Production"

from mllib.market_matrix import MarketMatrix
from mllib.topic_modeling import TopicModeling
import time

if __name__ == '__main__':
    start_total = time.time()
    start = time.time()
    mm = MarketMatrix(dbname='TwitterDB')

    #entire vocabulary
    mm.build()
    end = time.time()
    print 'Build time:', (end - start)
    start = time.time()

    #without creating the market matrix file
    id2word, id2tweetID, corpus = mm.buildTFMM()

    end = time.time()
    print 'Construct TF MM time:', (end - start)
    topic_model = TopicModeling(id2word=id2word, corpus=corpus)

    print 'LDA'
    start = time.time()
    for topic in topic_model.topicsLDA(num_topics=50):
        print topic
    end = time.time()
    print 'LDA TF time:', (end - start)
    """
    print 'LSI:'
    start = time.time()
    for topic in topic_model.topicsLSI():
        print topic
    end = time.time()
    print 'LSI TF time:', (end - start)

    print 'HDP:'
    start = time.time()
    for topic in topic_model.topicsHDP():
        print topic
    end = time.time()
    print 'HDP Count time:', (end - start)

    end_total = time.time()
    print 'total time:', (end_total - start_total)
    """