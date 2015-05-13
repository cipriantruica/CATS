import pymongo
import time
from pandas import *
import scipy.io, scipy.sparse
from gensim.corpora import MmCorpus
from gensim.models import LdaMulticore
from multiprocessing import cpu_count
from indexing.vacabulary_index import 

start = time.time() 


#query_and = {"$and": [{ "words.word": "shit"}, {'words.word': "fuck" } ], "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
#cursor = db.documents.find(query_and, {'words.count': 1, 'words.word': 1})

#query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
#cursor = db.documents.find({}, {'words.count': 1, 'words.word': 1})

class BuildMarketMatrix:
	def __init__(self, dbname='TwitterDB'):
		client = pymongo.MongoClient()
		self.db = client[dbname]

	def build(self, query=None, limit = 10000):
		cursor = None
		if query:
			cursor = db.vocabulary_query.find(fields={'word': 1, 'docIDs.docID': 1, 'docIDs.count': 1}, limit=1000, sort=[('idf',pymongo.ASCENDING)])
		else:
			cursor = db.vocabulary.find(fields={'word': 1, 'docIDs.docID': 1, 'docIDs.count': 1}, limit=1000, sort=[('idf',pymongo.ASCENDING)])
"""
dick = {}	
for elem in cursor:
	d = {}
	for e in elem['words']:
		d[e['word']] = e['count']
	dick[elem['_id']]  = d

df = DataFrame(dick).T.fillna(0)
print(df.columns.values)
id2word = {}
count = 0
for word in df.columns.values:
	id2word[count] = word
	count += 1

	
scipy.io.mmwrite("mmout_sparse", scipy.sparse.csr_matrix(df))
corpus = MmCorpus('mmout_sparse.mtx')



workers = cpu_count()
lda = LdaMulticore(corpus, num_topics=10, id2word=id2word,workers=workers)
for i in lda.show_topics():
	print i, "\n"

end = time.time() 
print "time_populate.append(", (end - start), ")"
"""

#this are just tests
if __name__ == '__main__':
	mm = BuildMarketMatrix(dbname='TwitterDB')
	mm.build()
	query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
	query_and = {"$and": [{ "words.word": "shit"}, {'words.word': "fuck" } ], "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
	mm.build(query_or)
	mm.build(query_and)
