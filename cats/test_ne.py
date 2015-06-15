__author__ = 'sheepman'

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

    ne = NEIndex(dbname)
    ne.createIndex(query)

    cursor = db.named_entities.find()
    start = time.time()
    idx = 0
    for elem in cursor:
        print elem['entity'], elem['count'], elem['type']
    end = time.time()
    print 'Time :', (end-start)
