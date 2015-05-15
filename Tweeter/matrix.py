import pymongo
import time
from pandas import *
import scipy.io, scipy.sparse
from gensim.corpora import MmCorpus
from gensim.models import LdaMulticore
from multiprocessing import cpu_count

start = time.time() 
dbname = 'TwitterDB'
client = pymongo.MongoClient()
db = client[dbname]

#query_and = {"$and": [{ "words.word": "shit"}, {'words.word': "fuck" } ], "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
#cursor = db.documents.find(query_and, {'words.count': 1, 'words.word': 1})

query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
cursor = db.documents.find({}, {'words.count': 1, 'words.word': 1})

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

"""
for tweetID, word in sorted(dick.items()):
	for word in words:
		if dick[tweetID].get(word, 0) == 0:
			dick[tweetID][word] = 0
for elem in dick:
	print elem, dick[elem]
print '*********************************'
print '*********************************'
print mm2
"""
end = time.time() 
print "time_populate.append(", (end - start), ")"