# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.com"
__status__ = "Production"

import pymongo
import time
from pandas import *
import scipy.io, scipy.sparse
from gensim.corpora import MmCorpus
from gensim.models import LdaMulticore
from multiprocessing import cpu_count
from twitter.indexing.vocabulary_index import VocabularyIndex

start = time.time() 
"""
RIP (RESEARCH IN PROGRESS) :)
"""

#query_and = {"$and": [{ "words.word": "shit"}, {'words.word': "fuck" } ], "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
#cursor = db.documents.find(query_and, {'words.count': 1, 'words.word': 1})

#query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
#cursor = db.documents.find({}, {'words.count': 1, 'words.word': 1})

class MarketMatrix:
    def __init__(self, dbname='TwitterDB'):
        client = pymongo.MongoClient()
        self.dbname = dbname
        self.db = client[self.dbname]
        self.cursor = None

    """
        input:
            query: a query used to build the vocabulary, if no query is given then we use the entire vocabulary
            limit: parameter used to limit the numeber of returned line, based on idf
            rebuild: parameter used if the vocabulary should be rebuilt        
    """
    def build(self, query=None, limit = 10000, rebuild = False):
        if query:
            #if the vocabulary should be rebuilt
            if rebuild:
                vocab = VocabularyIndex(self.dbname)
                vocab.createIndex(query)
            self.cursor = self.db.vocabulary_query.find(fields={'word': 1, 'idf': 1, 'docIDs.docID': 1, 'docIDs.count': 1, 'docIDs.tf': 1}, limit=limit, sort=[('idf',pymongo.ASCENDING)])
        else:
            #if the vocabulary should be rebuilt
            if rebuild:
                vocab = VocabularyIndex(self.dbname)
                vocab.createIndex()
            self.cursor = self.db.vocabulary.find(fields={'word': 1, 'idf': 1, 'docIDs.docID': 1, 'docIDs.count': 1, 'docIDs.tf': 1}, limit=limit, sort=[('idf',pymongo.ASCENDING)])    

    """
        constructs the binary market matrix
        output:
            the binary market matrix
    """
    def getBinaryMM(self):
        if self.cursor:
            self.cursor.rewind()
            total = 0;
            mm = {}            
            for elem in self.cursor:
                total += len(elem['docIDs'])
                for doc in elem['docIDs']:
                    #dictionary with {docID: {word1: 1, word2: 1}, ...}, only for words that exist
                    if mm.get(doc['docID'], -1) == -1:
                        mm[doc['docID']] = {elem['word']: 1}
                    else:
                        mm[doc['docID']][elem['word']] = 1
            print total
            return mm
            
    """
        constructs the count market matrix
        output:
            the count market matrix
    """
    def getCountMM(self):
        if self.cursor:
            self.cursor.rewind()
            mm = {}
            for elem in self.cursor:
                for doc in elem['docIDs']:
                    #dictionary with {docID: {word1: count_word1, word2: count_word2}, ...}
                    if mm.get(doc['docID'], -1) == -1:
                        mm[doc['docID']] = {elem['word']: doc['count']}
                    else:
                        mm[doc['docID']][elem['word']] = doc['count']
            return mm
    """
        constructs the TF market matrix
        output:
            the TF market matrix
    """
    def getTFMM(self):
        if self.cursor:
            self.cursor.rewind()
            mm = {}
            for elem in self.cursor:
                for doc in elem['docIDs']:
                    #dictionary with {docID: {word1: tf_word1, word2: tf_word2}, ...}
                    if mm.get(doc['docID'], -1) == -1:
                        mm[doc['docID']] = {elem['word']: doc['tf']}
                    else:
                        mm[doc['docID']][elem['word']] = doc['tf']
            return mm
    """
        writes the matrix to a file on disk
        input:
            filename for the binary mm output
        output:
            a id2word dictionary
            a id2twetID dictionary
    """
    def saveMM(self, matrix, filename):
        df = DataFrame(matrix).T.fillna(0)
        #print(df.columns.values)
        #print(df.index.values)
        scipy.io.mmwrite(filename, scipy.sparse.csr_matrix(df))
        id2word = {}
        count = 0
        for word in df.columns.values:
            id2word[count] = word
            count += 1
        count = 0
        id2tweetID = {}
        for tweetID in df.index.values:
            id2tweetID[count] = tweetID
            count += 1
        return id2word, tweetID


#these are just tests
if __name__ == '__main__':
    mm = MarketMatrix(dbname='TwitterDB')
    #mm.build()
    #query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
    query_and = {"$and": [{ "words.word": "shit"}, {'words.word': "fuck" } ], "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
    #mm.build(query_or)
    mm.build(query=query_and, limit=100)
    
    matrix = mm.getBinaryMM()
    mm.saveMM(matrix=matrix, filename='mm_binary')    
    matrix = mm.getCountMM()
    mm.saveMM(matrix=matrix, filename='mm_count')    
    matrix = mm.getTFMM()
    mm.saveMM(matrix=matrix, filename='mm_tf')    
    
