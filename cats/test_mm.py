from time import time
from mllib.market_matrix import MarketMatrix

# these are just tests
if __name__ == '__main__':
    query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
    query_and = {"$and": [{"words.word": "shit"}, {'words.word': "fuck"}],
                 "date": {"$gt": "2015-04-10", "$lte": "2015-04-12"}}
    #for the entire vocabulary
    start = time()
    mm = MarketMatrix(dbname='TwitterDB')

    mm.build(query=query_or)
    #mm.build(query=query_and, limit=100)
    end = time()
    print 'Build time:',(end-start)

    start = time()
    mm.buildBinaryMM('mm_binary.mtx')
    end = time()
    print "Binary MM time:", (end-start)
