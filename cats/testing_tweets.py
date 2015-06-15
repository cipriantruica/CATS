# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import time
import utils
from ddl_mongo import *
from models.mongo_models import *
from indexing.vocabulary_index import VocabularyIndex as VI
from indexing.ne_index import VocabularyIndex as NE
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor

"""
import sys
import threading
from datetime import timedelta
from multiprocessing.pool import ThreadPool
from indexing.inverted_index import InvertedIndex as IV
from indexing.pos_index import POSIndex as PI
"""

def getDates():
    documents = Documents.objects.only("createdAt")
    no_docs = documents.count()
    last_docDate = None
    if no_docs > 0:
        last_docDate = documents[no_docs-1].createdAt
    return last_docDate
    """
    last_wordDate = None
    words = Words.objects.only("createdAt")
    no_words = words.count()
    if no_words > 0:
        last_wordDate = words[no_words-1].createdAt
    return last_docDate, last_wordDate
    """



#try to parallelize this
def populateDB(filename, csv_delimiter, header, language='EN', dbname='TwitterDB', mode=0, k = 100):
    start = time.time() 
    h, lines = utils.readCSV(filename, csv_delimiter, header)
    populateDatabase(lines, language, dbname, mode)

    end = time.time() 
    print "time_populate.append(", (end - start), ")"

def updateIndexes(dbname, startDate):
    start = time.time()
    vocab = VI(dbname)
    vocab.updateIndex(startDate)
    end = time.time()
    print "vocabulary_update.append(", (end - start) , ")"

def deleteIndexes(dbname, docIDs):
    start = time.time()
    vocab = VI(dbname)
    vocab.deleteIndex(docIDs)
    end = time.time()
    print "vocabulary_delete.append(", (end - start) , ")"

def constructIndexes(dbname):
    #build Vocabulary
    start = time.time()
    vocab = VI(dbname)
    vocab.createIndex()
    end = time.time()
    print "vocabulary_build.append(", (end - start) , ")"

    # built the NE Index
    start = time.time()
    ner = NE(dbname)
    ner.createIndex()
    end = time.time()
    print "vocabulary_build.append(", (end - start) , ")"
    """
    start = time.time()
    iv = IV(dbname)
    iv.createIndex()
    end = time.time()
    print "inverted_build.append(", (end - start) , ")"
    
    start = time.time()
    pi = PI(dbname)
    pi.createIndex()
    end = time.time()
    print "pos_build.append(", (end - start) , ")"
    """

def deleteDocuments(startDate):
    docIDs = []
    documents = Documents.objects(Q(createdAt__gt = startDate)).only("id")
    for document in documents:
        docIDs.append(document.id)
        document.delete()
    return docIDs
    
def main(filename, csv_delimiter = '\t', header = True, dbname = 'TwitterDB', language='EN', initialize = 0, mode=0, deleteDate=None):
    connectDB(dbname)
    print mode
    #initialize everything from the stat
    if initialize == 0:
        Documents.drop_collection()
        populateDB(filename, csv_delimiter, header, language, dbname=dbname, mode=mode)
        constructIndexes(dbname)
    elif initialize == 1: #update the database with new documents, should work, not tested
        last_docDat = getDates()
        populateDB(filename, csv_delimiter, header, language, mode=mode)
        Documents.objects(intText__exists = False).delete()
        updateIndexes(dbname, last_docDat)
    elif initialize == 2: #update the database after documents are deleted, should work, not tested
        if deleteDate:
            docIDs = deleteDocuments(deleteDate)
            deleteIndexes(dbname, docIDs)

# this script receives 7 parameters
# 1 - filename
# 2 - the csv delimiter: t - tab, c - coma, s - semicolon
# 3 - integer: 1 csv has header, 0 csv does not have hearer
# 4 - integer: - nr of threads
# 5 - language: EN or FR
# 6 - integer: 0 - create the database, 1 - update the database
# 7 - integer: 0 - use fast lemmatizer (not accurate), 1 - use slow lemmatizer (accurate)
if __name__ == "__main__":
    filename = sys.argv[1] 
    csv_delimiter = utils.determineDelimiter(sys.argv[2])
    header = bool(sys.argv[3])
    dbname = sys.argv[4]
    language = sys.argv[5] #currently EN & FR, FR does not work so well
    initialize = int(sys.argv[6])
    mode = int(sys.argv[7])
    main(filename=filename, csv_delimiter=csv_delimiter, header=header, dbname=dbname, language=language, initialize=initialize, mode=mode)
