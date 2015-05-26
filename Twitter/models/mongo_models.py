# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

from mongoengine import *
from datetime import datetime
from bson.objectid import ObjectId
import pymongo

def connectDB(dbname = 'TwitterDB'):
	connect(dbname, host="127.0.0.1", port=27017, read_preference= True)

class Word(EmbeddedDocument):
	_auto_id_field = False
	word = StringField(max_length = 255)
	pos = ListField()
	count = FloatField()
	tf = FloatField()
	idf = FloatField()

	meta = {
		'ordering': ['+word']
	}

class Documents(Document):
	_auto_id_field = False
	tweetID = StringField(max_length = 255, required = True, unique=True)
	rawText = StringField()
	cleanText = StringField() #intermediate text without stopwords, punctuation, etc
	lemmaText = StringField() #lemma text
	#the date the element was inserted in the database
	createdAt = DateTimeField(default=datetime.now)
	gender = StringField()
	hashtags = ListField()
	attags = ListField()
	date = DateTimeField()
	language = StringField()
	author = StringField()
	tags = ListField()
	words = ListField(EmbeddedDocumentField("Word"))
	

	meta = {
		'ordering': ['+createdAt']
	}


class InvertedIndex(Document):
	word = StringField(max_length = 255, required = True, unique=True)
	docIDs = ListField()
	createdAt = DateTimeField(default=datetime.now) 

	meta = { 
			'ordering': ['+createdAt']
	}

class Docs(EmbeddedDocument):
	_auto_id_field = False
	docID = ObjectIdField()
	count = FloatField()
	tf = FloatField()
	wtype = StringField(max_length = 255)

class Vocabulary(Document):
	word = StringField(max_length = 255, required = True, unique=True)
	idf = FloatField()
	#wtype = StringField(max_length = 255, required = True) #not yet implemented
	createdAt = DateTimeField(default=datetime.now)
	docIDs = ListField(EmbeddedDocumentField("Docs"))

	meta = {
			'indexes': [
				{
					'fields': ['+word'],
					'unique': True,
					'sparse': False
				}
		]
	}

class NamedEntities(Document):
	docID = ObjectIdField()
	createdAt = DateTimeField(default=datetime.now)
	gpe = ListField()
	person = ListField()
	organization = ListField()
	facility = ListField()
	location = ListField()
