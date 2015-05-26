# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@gmail.com"
__status__ = "Production"

import pymongo
from twitter.indexing.vocabulary_index import VocabularyIndex

#TO DO
#write a single function to write to file

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

	def build(self, query=None, limit=10000, rebuild=False):
		if query:
			# if the vocabulary should be rebuilt
			if rebuild:
				vocab = VocabularyIndex(self.dbname)
				vocab.createIndex(query)
			self.cursor = self.db.vocabulary_query.find(
				fields={'word': 1, 'idf': 1, 'docIDs.docID': 1, 'docIDs.count': 1, 'docIDs.tf': 1}, limit=limit, sort=[('idf', pymongo.ASCENDING)])
		else:
			# if the vocabulary should be rebuilt
			if rebuild:
				vocab = VocabularyIndex(self.dbname)
				vocab.createIndex()
			self.cursor = self.db.vocabulary.find(
				fields={'word': 1, 'idf': 1, 'docIDs.docID': 1, 'docIDs.count': 1, 'docIDs.tf': 1}, limit=limit, sort=[('idf', pymongo.ASCENDING)])

	"""
        constructs the binary market matrix
        output:
            the binary market matrix
    """

	def buildBinaryMM(self, filename='mm_binary.mtx'):
		if self.cursor:
			self.cursor.rewind()
			no_entries = 0
			id2word = {}
			word2id = {}
			wordID = 0
			id2tweetID = {}
			tweetID2id = {}
			tweetID = 0
			mm = {}
			for elem in self.cursor:
				no_entries += len(elem['docIDs'])
				if word2id.get(elem['word'], -1) == -1:
					id2word[wordID] = elem['word']
					word2id[elem['word']] = wordID
					wordID += 1
				for doc in elem['docIDs']:
					if tweetID2id.get(doc['docID'], -1) == -1:
						id2tweetID[tweetID] = doc['docID']
						tweetID2id[doc['docID']] = tweetID
						tweetID += 1
					# dictionary with {docID: {word1: 1, word2: 1}, ...}, only for words that exist
					if mm.get(tweetID2id[doc['docID']], -1) == -1 :
						mm[tweetID2id[doc['docID']]] = {word2id[elem['word']]: 1}
					else:
						mm[tweetID2id[doc['docID']]][word2id[elem['word']]] = 1
			with open(filename, 'w') as file:
				file.write('%%MatrixMarket matrix coordinate real general\n%\n')
				file.write(str(len(id2tweetID)) + ' ' +  str(len(id2word)) + ' ' + str(no_entries) + '\n')
				for doc in mm:
					for word in mm[doc]:
						file.write(str(doc + 1) + ' ' + str(word + 1) + ' ' + str(mm[doc][word]) + '\n')
				file.close()
			return id2word, id2tweetID, mm

	"""
        constructs the count market matrix
        output:
            the count market matrix
    """

	def buildCountMM(self, filename='mm_count.mtx'):
		if self.cursor:
			self.cursor.rewind()
			no_entries = 0
			id2word = {}
			word2id = {}
			wordID = 0
			id2tweetID = {}
			tweetID2id = {}
			tweetID = 0
			mm = {}
			for elem in self.cursor:
				no_entries += len(elem['docIDs'])
				if word2id.get(elem['word'], -1) == -1:
					id2word[wordID] = elem['word']
					word2id[elem['word']] = wordID
					wordID += 1
				for doc in elem['docIDs']:
					if tweetID2id.get(doc['docID'], -1) == -1:
						id2tweetID[tweetID] = doc['docID']
						tweetID2id[doc['docID']] = tweetID
						tweetID += 1
					# dictionary with {docID: {word1: 1, word2: 1}, ...}, only for words that exist
					if mm.get(tweetID2id[doc['docID']], -1) == -1 :
						mm[tweetID2id[doc['docID']]] = { word2id[elem['word']]: doc['count'] }
					else:
						mm[tweetID2id[doc['docID']]][word2id[elem['word']]] = doc['count']

			with open(filename, 'w') as file:
				file.write('%%MatrixMarket matrix coordinate real general\n%\n')
				file.write(str(len(id2tweetID)) + ' ' +  str(len(id2word)) + ' ' + str(no_entries) + '\n')
				for doc in mm:
					for word in mm[doc]:
						file.write(str(doc + 1) + ' ' + str(word + 1) + ' ' + str(mm[doc][word]) + '\n')
				file.close()
			return id2word, id2tweetID, mm

	"""
        constructs the TF market matrix
        output:
            the TF market matrix
    """
	def buildTFMM(self, filename='mm_tf.mtx'):
		if self.cursor:
			self.cursor.rewind()
			no_entries = 0
			id2word = {}
			word2id = {}
			wordID = 0
			id2tweetID = {}
			tweetID2id = {}
			tweetID = 0
			mm = {}
			for elem in self.cursor:
				no_entries += len(elem['docIDs'])
				if word2id.get(elem['word'], -1) == -1:
					id2word[wordID] = elem['word']
					word2id[elem['word']] = wordID
					wordID += 1
				for doc in elem['docIDs']:
					if tweetID2id.get(doc['docID'], -1) == -1:
						id2tweetID[tweetID] = doc['docID']
						tweetID2id[doc['docID']] = tweetID
						tweetID += 1
					# dictionary with {docID: {word1: 1, word2: 1}, ...}, only for words that exist
					if mm.get(tweetID2id[doc['docID']], -1) == -1 :
						mm[tweetID2id[doc['docID']]] = {word2id[elem['word']]: doc['tf']}
					else:
						mm[tweetID2id[doc['docID']]][word2id[elem['word']]] = doc['tf']
			with open(filename, 'w') as file:
				file.write('%%MatrixMarket matrix coordinate real general\n%\n')
				file.write(str(len(id2tweetID)) + ' ' +  str(len(id2word)) + ' ' + str(no_entries) + '\n')
				for doc in mm:
					for word in mm[doc]:
						file.write(str(doc+1) + ' ' + str(word+1) + ' ' + str(int(mm[doc][word])) + '\n')
				file.close()
			return id2word, id2tweetID, mm

# this are just tests
if __name__ == '__main__':
	mm = MarketMatrix(dbname='TwitterDB')
	query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
	query_and = {"$and": [{"words.word": "shit"}, {'words.word': "fuck"}],
				 "date": {"$gt": "2015-04-10", "$lte": "2015-04-12"}}
	#for the entire vocabulary
	#mm.build()
	#mm.build(query_or)
	mm.build(query=query_and, limit=100)
	#print "Binary MM"
	#mm.buildBinaryMM()
	#print "Binary Count"
	#mm.buildCountMM()
	print "Binary TF"
	mm.buildTFMM()

