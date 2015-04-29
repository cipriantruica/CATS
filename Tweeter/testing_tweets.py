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

def populateDB(filename, csv_delimiter, header, language):
	start = time.time() 
	h, lines = utils.readCSV(filename, csv_delimiter, header)
	for line in lines:
		populateDatabase(line, language)
	end = time.time() 
	print "time_populate.append(", (end - start), ")"

def clean(language, last_docDate=None):
	if not last_docDate:
		documents = Documents.objects.only("createdAt")
	else:
		documents = Documents.objects(Q(createdAt__gte = last_docDate)).only("createdAt")
	no_docs = documents.count()
	print no_docs
	
	list_of_dates = []
	idx = 0
	for document in documents:		
		if idx%100 == 0 or idx + 1 == no_docs:
			list_of_dates.append(document.createdAt)
		idx += 1
	#add one second to the last date
	list_of_dates[-1] += timedelta(0,1)
	
	#create clean text in chunks
	start = time.time() 
	for idx in xrange(0, len(list_of_dates)-1, 1) :
		createCleanTextField(list_of_dates[idx], list_of_dates[idx+1], language)
	
	end = time.time() 
	print "time_cleantext.append(", (end - start), ")"
	
	#delete documents without cleanText
	Documents.objects(cleanText__exists = False).delete();

#this does not work yet
def buildNamedEntities():
	

	documents = Documents.objects.only("createdAt")
	no_docs = documents.count()
	
	list_of_dates = []
	idx = 0

	for document in documents:		
		if idx%100 == 0 or idx + 1 == no_docs:
			list_of_dates.append(document.createdAt)
		idx += 1
	#add one second to the last date
	list_of_dates[-1] += timedelta(0,1)
	
	no_threads = cpu_count()
		
	start = time.time()
	with ThreadPoolExecutor(max_workers = no_threads) as e:
		for idx in xrange(0, len(list_of_dates)-1, 1) :
			 e.submit(createNamedEntitiesCollection, list_of_dates[idx], list_of_dates[idx+1])
	end = time.time() 
	
	print "time build named entities:", (end - start) 

def constructIndexes(dbname):
	start = time.time()
	vocab = VI(dbname)
	vocab.createIndex()
	end = time.time()
	print "vocabulary build time:", (end - start) 

def updateIndexes(dbname, startDate):
	start = time.time()
	vocab = VI(dbname)
	vocab.updateIndex(startDate)
	end = time.time()
	print "vocabulary build time:", (end - start) 

	
def main(filename, csv_delimiter = '\t', header = True, dbname = 'ERICDB', language='EN', initialize = 0):
	connectDB(dbname)	
	#initialize everything from the stat
	if initialize == 0:
		Documents.drop_collection() 
		Words.drop_collection()	
		populateDB(filename, csv_delimiter, header, language)
		Documents.objects(intText__exists = False).delete()
		clean(language)
		constructIndexes(dbname)
	elif initialize == 1: #update the database with new infomation not tested, should work
		last_docDate, last_wordDate = getDates()
		populateDB(filename, csv_delimiter, header, language)
		Documents.objects(intText__exists = False).delete()
		clean(language, last_docDate)
		updateIndexes(dbname, last_wordDate)

	#this does not work yet
	#NamedEntities.drop_collection()
	#buildNamedEntities()

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
