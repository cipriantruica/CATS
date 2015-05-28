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
from market_matrix import MarketMatrix
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
    def __init__(self, id2word, corpus=None, filename=None):
        if corpus:
            self.corpus = corpus
        if filename:
            self.corpus = MmCorpus(filename)
        self.id2word = id2word

    def topicsLDA(self, num_topics=10, num_iterations=10000):
        workers = cpu_count()
        topic_model = LdaMulticore(corpus=self.corpus, num_topics=num_topics, id2word=self.id2word, iterations=num_iterations, workers=workers)
        for topic in topic_model.show_topics():
            print topic


    def topicsLSI(self, num_topics=10):
        lsi = LsiModel(corpus=self.corpus, num_topics=num_topics, id2word=self.id2word)
        for topic in lsi.show_topics():
            print topic


# these are just tests
if __name__ == '__main__':
    query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
    query_and = {"$and": [{"words.word": "shit"}, {'words.word': "fuck"}], "date": {"$gt": "2015-04-10", "$lte": "2015-04-12"}}

    start_total = time.time()

    start = time.time()
    mm = MarketMatrix(dbname='TwitterDB')
    
    #with query + rebuild vocabulary
    #mm.build(query=query_and, rebuild=True)
    #mm.build(query=query_or, rebuild=True)
    
    #entire vocabulary
    mm.build()

    end = time.time()
    print 'Build time:', (end - start)

    start = time.time()

    #create market matrix file
    #filename = 'mm_count2.mm'
    #id2word, id2tweetID, corpus = mm.buildBinaryMM(filename=filename)
    #topic_model = TopicModeling(id2word=id2word, filename=filename)

    #without creating the file
    id2word, id2tweetID, corpus = mm.buildCountMM()
    end = time.time()
    print 'Construct Count MM time:', (end - start)

    topic_model = TopicModeling(id2word=id2word, corpus=corpus)

    start = time.time()
    topic_model.topicsLDA()
    end = time.time()
    print 'LDA Count time:', (end - start)

    start = time.time()
    topic_model.topicsLSI()
    end = time.time()
    print 'LSI Count time:', (end - start)

    start = time.time()

    #create market matrix file
    #filename = 'mm_binary2.mm'
    #id2word, id2tweetID, corpus = mm.buildBinaryMM(filename=filename)
    #topic_model = TopicModeling(id2word=id2word, filename=filename)

    #without creating the market matrix file
    id2word, id2tweetID, corpus = mm.buildBinaryMM()

    end = time.time()
    print 'Construct Binary MM time:', (end - start)

    topic_model = TopicModeling(id2word=id2word, corpus=corpus)

    start = time.time()
    topic_model.topicsLDA()
    end = time.time()
    print 'LDA Binary time:', (end - start)

    start = time.time()
    topic_model.topicsLSI()
    end = time.time()
    print 'LSI Binary time:', (end - start)

    start = time.time()

    #create market matrix file
    #filename = 'mm_tf2.mm'
    #id2word, id2tweetID, corpus = mm.buildTFMM(filename=filename)
    #topic_model = TopicModeling(id2word=id2word, filename=filename)

    #without creating the market matrix file
    id2word, id2tweetID, corpus = mm.buildTFMM()

    end = time.time()
    print 'Construct TF MM time:', (end - start)

    topic_model = TopicModeling(id2word=id2word, corpus=corpus)

    start = time.time()
    topic_model.topicsLDA()
    end = time.time()
    print 'LDA TF time:', (end - start)

    start = time.time()
    topic_model.topicsLSI()
    end = time.time()
    print 'LSI TF time:', (end - start)

    end_total = time.time()
    print 'total time:', (end_total - start_total)
