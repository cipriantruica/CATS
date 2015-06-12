from time import time
from mllib.market_matrix import MarketMatrix

# these are just tests
if __name__ == '__main__':
    #for the entire vocabulary
    start = time()
    mm = MarketMatrix(dbname='TwitterDB')
    mm.build()
    #mm.build(query=query_or)
    #mm.build(query=query_and, limit=100)
    end = time()
    print 'Build time:',(end-start)
    start = time()
    mm.buildBinaryMM('mm_binary.mtx')
    end = time()
    print "Binary MM time:", (end-start)
