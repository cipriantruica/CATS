# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import sys
import threading
import time
import gc
import shutil
from datetime import timedelta
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from ddl_mongo import *
from models.mongo_models import *
from indexing.vocabulary_index import VocabularyIndex as VI
from indexing.inverted_index import InvertedIndex as IV
from indexing.pos_index import POSIndex as PI


def getDates():
	documents = Documents.objects.only("createdAt")
	no_docs = documents.count()
	last_docDate = None
	last_wordDate = None
	if no_docs > 0:
		last_docDate = documents[no_docs-1].createdAt
	words = Words.objects.only("createdAt")
	no_words = words.count()
	if no_words > 0:
		last_wordDate = words[no_words-1].createdAt
	return last_docDate, last_wordDate

#try to parallelize this
def populateDB(filename, csv_delimiter, header, language, k = 1000):
	start = time.time() 
	h, lines = utils.readCSV(filename, csv_delimiter, header)
	populateDatabase(lines, language)
	#noLines = (len(lines)/k)+1
	#print noLines, len(lines[0: 1000])
	#for idx in range(0, noLines):
	#	start, end = idx*k, idx*k+k
	#	if end<=noLines:
	#		populateDatabase(lines[start:end], language)
	#	else:
	#		populateDatabase(lines[start:], language)
	#	print idx, idx*k, idx*k+k
	#	for elem in lines[start: end]:
	#		print elem
	#for idx in range(0, noLines):
	#	start, end = idx*k, idx*k+k
	#	print idx, idx*k, idx*k+k
	#	if end<=noLines:
	#		populateDatabase(lines[start:end], language)
	#	else:
	#		populateDatabase(lines[start:], language)
	end = time.time() 
	print "time_populate.append(", (end - start), ")"


def constructIndexes(dbname):
	start = time.time()
	vocab = VI(dbname)
	vocab.createIndex()
	end = time.time()

	print "vocabulary_build.append(", (end - start) , ")"	
	
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
	


	
def main(filename, csv_delimiter = '\t', header = True, dbname = 'TwitterDB', language='EN', initialize = 0):
	connectDB(dbname)	
	#initialize everything from the stat
	if initialize == 0:
		#Documents.drop_collection() 
		#populateDB(filename, csv_delimiter, header, language)
		constructIndexes(dbname)
	elif initialize == 1: #update the database with new infomation not tested, should work
		last_docDate, last_wordDate = getDates()
		populateDB(filename, csv_delimiter, header, language)
		Documents.objects(intText__exists = False).delete()
		clean(language, last_docDate)
		updateIndexes(dbname, last_wordDate)
		print 'date for update indexes:', last_wordDate
		print 'last date doc:', last_docDate
	
#this script receives 5 parameters
# 1 - filename
# 2 - the csv delimiter: t - tab, c - coma, s - semicolon
# 3 - integer: 1 csv has header, 0 csv does not have hearer
# 4 - integer: - nr of threads
# 5 - language: EN or FR
# 6 - integer: 0 - create the database, 1 - update the database
if __name__ == "__main__":
	filename = sys.argv[1] 
	csv_delimiter = utils.determineDelimiter(sys.argv[2])
	header = bool(sys.argv[3])
	dbname = sys.argv[4]
	language = sys.argv[5] #currently EN & FR, FR does not work so well
	initialize = int(sys.argv[6])
	main(filename, csv_delimiter, header, dbname, language, initialize)
