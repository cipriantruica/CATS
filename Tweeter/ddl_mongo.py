# coding: utf-8
import sys  
import utils
from models.mongo_models import *
from nlplib.lemmatize_text import LemmatizeText
from nlplib.named_entities import NamedEntitiesRegonizer
from nlplib.clean_text import CleanText

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2014, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"


reload(sys)  
sys.setdefaultencoding('utf8')

# params:
# list with the fallowing elemets:
# *elem[0] = title of the document
# *elem[1] = raw text of the document
# *elem[2] = the date inside the document
# *elem[3] = list of tags
# *elem[4] = list of authors
# language, default English
# TO_DO sould see if other fields are needed



ct = CleanText()
def populateDatabase(elems, language='EN', dbname='TwitterDB'):
	client = pymongo.MongoClient()
	db = client[dbname]
	if elems:
		documents = []
		#print len(elems)
		#idx = 1
		for elem in elems:
			if len(elem) >= 4:
				#get language
				if len(elem) >= 5:
					lang = elem[4]
				else:
					lang = language
				#get clean text
				cleanText, hashtags, attags = ct.cleanText(elem[1], lang)
				#if clean text exists
				if len(ct.removePunctuation(cleanText))>0:
					#extract lemmas and part of speech
					lemmas = LemmatizeText(ct.removePunctuation(cleanText), lang)
					lemmas.createLemmaText()
					lemmaText = lemmas.cleanText
					if lemmaText and lemmaText != " ":
						document = {}
						lemmas.createLemmas()
						words = []
						for w in lemmas.wordList:
							word = {}
							word['word']=w.word
							word['tf']=w.tf
							word['count']=w.count
							word['pos']=w.wtype
							words.append(word)
						#construct the document
						document['_id'] = elem[0]
						document['rawText'] = elem[1]
						document['cleanText'] = cleanText
						document['lemmaText'] = lemmaText
						document['date'] = elem[2]
						document['author'] = elem[3]
						document['words'] = words
						document['attags'] = attags
						document['hashtags'] = hashtags
						documents.append(document)
						#print idx
						#idx += 1
			else:
				try:
					print "tweet with problems: ", elem[0]
				except Exception, e:
					print e
		if documents:
			db.documents.insert( documents)

#this function will create the named_entities collection
def createNamedEntitiesCollection(startDate, endDate):
	documents = Documents.objects(Q(createdAt__gte = startDate) & Q(createdAt__lt = endDate)).only("id", "intText").timeout(False)	
	for document in documents:
		namedEntitiesProcess = NamedEntitiesRegonizer(document.intText)
		namedEntitiesProcess.createNamedEntities()
		namedEntity = NamedEntities()
		namedEntity.docID = document.id
		namedEntity.gpe = namedEntitiesProcess.gpe
		namedEntity.person = namedEntitiesProcess.person
		namedEntity.organization = namedEntitiesProcess.organization
		namedEntity.facility = namedEntitiesProcess.facility
		namedEntity.location = namedEntitiesProcess.location
		try:		
			namedEntity.save()
		except Exception as e:
			print "Update Error!!!", e
