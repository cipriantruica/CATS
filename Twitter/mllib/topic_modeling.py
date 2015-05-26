# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@gmail.com"
__status__ = "Production"

from gensim.corpora import MmCorpus
from gensim.models import LdaMulticore
from multiprocessing import cpu_count
from market_matrix import MarketMatrix as normal
from market_matrix_manual import MarketMatrix as manual


class LDA:
    def __init__(self, filename, id2word, no_topics = 10):
        self.filename = filename
        self.id2word = id2word
        self.no_topics = no_topics

    def topicModeling(self):
        corpus = MmCorpus(self.filename)
        workers = cpu_count()
        lda = LdaMulticore(corpus, num_topics=self.no_topics, id2word=self.id2word, workers=workers)
        for i in lda.show_topics():
            print i, "\n"

# this are just tests
if __name__ == '__main__':
    query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
    query_and = {"$and": [{"words.word": "shit"}, {'words.word': "fuck"}], "date": {"$gt": "2015-04-10", "$lte": "2015-04-12"}}

    print 'Generated MM'
    mm1 = normal(dbname='TwitterDB')
    mm1.build(query=query_and, rebuild=True)
    matrix1a = mm1.getCountMM()
    matrix1b = mm1.getBinaryMM()
    matrix1c = mm1.getTFMM()
    filename = 'mm_count1.mtx'
    id2word1, tweetID = mm1.saveMM(matrix=matrix1a, filename=filename)
    lda1 = LDA(filename=filename, id2word=id2word1)
    lda1.topicModeling()

    filename = 'mm_binary1.mtx'
    id2word1, tweetID = mm1.saveMM(matrix=matrix1b, filename=filename)
    lda1 = LDA(filename=filename, id2word=id2word1)
    lda1.topicModeling()

    filename = 'mm_tf1.mtx'
    id2word1, tweetID = mm1.saveMM(matrix=matrix1c, filename=filename)
    lda1 = LDA(filename=filename, id2word=id2word1)
    lda1.topicModeling()

    print 'Manual MM'
    mm2 = manual(dbname='TwitterDB')
    mm2.build(query=query_and, rebuild=True)
    filename = 'mm_count2.mtx'
    id2word2, id2tweetID, matrix = mm2.buildCountMM(filename=filename)
    lda2 = LDA(filename=filename, id2word=id2word2)
    lda2.topicModeling()

    filename = 'mm_binary2.mtx'
    id2word2, id2tweetID, matrix = mm2.buildBinaryMM(filename=filename)
    print id2word2
    lda2 = LDA(filename=filename, id2word=id2word2)
    lda2.topicModeling()

    filename = 'mm_tf2.mtx'
    id2word2, id2tweetID, matrix = mm2.buildTFMM(filename=filename)
    print id2word2
    lda2 = LDA(filename=filename, id2word=id2word2)
    lda2.topicModeling()
