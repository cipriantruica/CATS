from mongoengine import *
from datetime import datetime
from bson.objectid import ObjectId

def connectDB(dbname = 'ERICDB'):
	connect(dbname, host="127.0.0.1", port=27017, read_preference= True)

class Documents(Document):
	tweetID = StringField(max_length = 255, required = True, unique=True)
	rawText = StringField()
	intText = StringField() #intermediate text without stopwords, punctuation, etc
	cleanText = StringField() #lemma text
	#the date the element was inserted in the database
	createdAt = DateTimeField(default=datetime.now)
	date = DateTimeField()
	language = StringField()
	author = StringField()
	tags = ListField()
	#words = ListField(EmbeddedDocumentField("Word"))
	

	meta = {
		'ordering': ['+createdAt'],
		'indexes': [
			{
				'fields': ['+createdAt'],
				'unique': True,
				'sparse': False
			},
			
		]
	}

	"""
	{
				'fields': ['words']
			}
	,
	{
		'fields': ["$cleanText"],
		'default_language': 'english'
	},
	{
		'fields': ['words'],
		'unique': True,
		'sparse': False
	},
	{
		'fields': ['words.word'],
		'unique': True,
		'sparse': False
	}
	"""

class Word(EmbeddedDocument):
	_auto_id_field = False
	word = StringField(max_length = 255)
	wtype = ListField()
	count = FloatField()
	tf = FloatField()
	idf = FloatField()

	meta = {
		'ordering': ['-word'],
		'indexes': [		
			{
				'fields': ['words.word']
			}
		]
	}

class Words(Document):
	docID = ObjectIdField()
	createdAt = DateTimeField(default=datetime.now)
	words = ListField(EmbeddedDocumentField("Word"))

	meta = {
		'ordering': ['+createdAt']		
	}

class InvertedIndex(Document):
	word = StringField(max_length = 255, required = True, unique=True)
	docIDs = ListField()
	createdAt = DateTimeField(default=datetime.now) 

	meta = { 
			'ordering': ['+createdAt'], 
#			'indexes': [
#				{
#					'fields': ['+createdAt'],
#					'unique': True,
#					'sparse': False
#				}
#		]
	}

class Docs(EmbeddedDocument):
	_auto_id_field = False
	#docId = ReferenceField("Documents", dbref=False)
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
