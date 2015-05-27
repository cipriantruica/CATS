# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.com"
__status__ = "Production"

from gensim.corpora import MmCorpus
from gensim.models import LdaMulticore
from gensim.models import LsiModel
from multiprocessing import cpu_count
from market_matrix import MarketMatrix as normal
from market_matrix_manual import MarketMatrix as manual
import time

"""
class for topic modeling
implemets:
- LDA (Latent Dirichlet Allocation)
- LSI (Latent Semantic Indexing)

Params:
    - id2words - id with
    - filename - that points to the location of a Market Matrix file (slower)
    - corpus - in memory corpus list of list of sets where a set contains the word id and its weight (faster)
    e.g. [[(),(),...,()],[(),(),...,()],[(),(),...,()],...,[(),(),...,()]]

    use either the filename or the corpus

"""

class TopicModeling:
    def __init__(self, id2word, corpus = None, filename = None):
        if corpus:
            self.corpus = corpus
        if filename:
            self.corpus = MmCorpus(filename)
        self.id2word = id2word

    def topicsLDA(self, num_topics = 10):
        workers = cpu_count()
        lda = LdaMulticore(corpus = self.corpus, num_topics = num_topics, id2word = self.id2word, workers = workers)
        for topic in lda.show_topics():
            print topic


    def topicsLSI(self, num_topics = 10):
        lsi = LsiModel(corpus = self.corpus, num_topics = num_topics, id2word = self.id2word)
        for topic in lsi.show_topics():
            print topic


# these are just tests
if __name__ == '__main__':
    query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
    query_and = {"$and": [{"words.word": "shit"}, {'words.word': "fuck"}], "date": {"$gt": "2015-04-10", "$lte": "2015-04-12"}}
    """
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
    """
    print 'Manual MM'
    start_total = time.time()

    start_build = time.time()
    mm2 = manual(dbname='TwitterDB')
    #mm2.build(query=query_and, rebuild=True)
    #entire vocabulary
    mm2.build()
    end_build = time.time()
    print 'Build time:', (end_build - start_build)

    filename = 'mm_count2.mm'

    id2word2, id2tweetID, matrix, corpus = mm2.buildCountMM(filename=filename)
    #lda2 = TopicModeling(id2word=id2word2, filename=filename)
    lda2 = TopicModeling(id2word=id2word2, corpus=corpus)
    start_count1 = time.time()
    lda2.topicsLDA()
    end_count1 = time.time()
    print 'LDA Count time:', (end_count1 - start_count1)

    start_count2 = time.time()
    lda2.topicsLSI()
    end_count2 = time.time()
    print 'LSI Count time:', (end_count2 - start_count2)

    filename = 'mm_binary2.mm'

    id2word2, id2tweetID, matrix, corpus = mm2.buildBinaryMM(filename=filename)
    #lda2 = TopicModeling(id2word=id2word2, filename=filename)
    lda2 = TopicModeling(id2word=id2word2, corpus=corpus)
    start_binary1 = time.time()
    lda2.topicsLDA()
    end_binary1 = time.time()
    print 'LDA Binary time:', (end_binary1 - start_binary1)

    start_binary2 = time.time()
    lda2.topicsLSI()
    end_binary2 = time.time()
    print 'LSI Binary time:', (end_binary2 - start_binary2)

    filename = 'mm_tf2.mm'

    id2word2, id2tweetID, matrix, corpus = mm2.buildTFMM(filename=filename)
    #lda2 = TopicModeling(id2word=id2word2, filename=filename)
    lda2 = TopicModeling(id2word=id2word2, corpus=corpus)
    start_tf1 = time.time()
    lda2.topicsLDA()
    end_tf1 = time.time()
    print 'LDA TF time:', (end_tf1 - start_tf1)

    start_tf2 = time.time()
    lda2.topicsLSI()
    end_tf2 = time.time()
    print 'LSI TF time:', (end_tf2 - start_tf2)

    end_total = time.time()
    print 'total time:', (end_total - start_total)