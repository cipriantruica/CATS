# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
import time
from indexing.ne_index import NEIndex

if __name__ == '__main__':
    client = pymongo.MongoClient()
    dbname = 'TwitterDB'
    db = client[dbname]
    #words with or
    query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}, 'namedEntities': {'$exists': 'true'}}
    #words with and
    query_and = {"$and": [{ "words.word": "shit"}, {'words.word': "fuck" } ], "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}, 'namedEntities': {'$exists': 'true'}}
    query = {'namedEntities': {'$exists': 'true'}}

    start = time.time()
    ne = NEIndex(dbname)
    ne.createIndex(query)
    end = time.time()
    print 'NE creation time:', (end-start)

    start = time.time()
    cursor = db.named_entities.find(sort=[('count',pymongo.DESCENDING)])
    idx = 0
    for elem in cursor:
        print elem['entity'], elem['count'], elem['type']
    end = time.time()
    print 'Time :', (end-start)
