# coding: utf-8
import sys  
import utils
from models.mongo_models import *
from nlplib.lemmatize_text import LemmatizeText
from nlplib.named_entities import NamedEntitiesRegonizer
from nlplib.clean_text import CleanText

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

def populateDatabase(elem, language='EN'):
	if len(elem) > 0:
		cleanText = CleanText()
		tweetID = elem[0]
		document = Documents.objects(tweetID=tweetID).timeout(False)
			
		if not document:
			if len(elem) == 4:
				document = Documents()
				document.tweetID = tweetID
				document.rawText = elem[1]
				document.intText = cleanText.cleanText(elem[1], language)
				document.date = elem[2]
				document.author = elem[3]
				document.language = language
				try:
					document.save()
				except Exception as e:
					print "Insert Error!!!", e
			else:
				print "tweet with problems: ",tweetID
		


#this functions adds to the documents collection the cleanText and words labels
def createCleanTextField(startDate, endDate, language):
	documents = Documents.objects(Q(createdAt__gte = startDate) & Q(createdAt__lt = endDate)).only("id", "intText").timeout(False)
	for document in documents:
		if document.intText and document.intText != " ":
			lemmas = LemmatizeText(document.intText, language)
			lemmas.createLemmaText()
			if lemmas.cleanText and lemmas.cleanText != " ":
				wordsColl = Words()
				lemmas.createLemmas()
				words = [Word(word=word.word, tf=word.tf, count=word.count, wtype=word.wtype) for word in lemmas.wordList]
				wordsColl.docID = document.id
				wordsColl.words = words
				try:
					#update document
					#document.update(set__cleanText=lemmas.cleanText, set__words=words)
					document.update(set__cleanText=lemmas.cleanText)
					wordsColl.save()
				except Exception as e:
					print "Update Error!!!", e

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
