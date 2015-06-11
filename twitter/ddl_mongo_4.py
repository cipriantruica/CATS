# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import sys
from models.mongo_models import *
from nlplib.lemmatize_text import LemmatizeText
from nlplib.named_entities import NamedEntitiesRegonizer
from nlplib.clean_text import CleanText
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import time

reload(sys)
sys.setdefaultencoding('utf8')

ct = CleanText()

# params:
# elems is list of lists:
#   !!! KEEP THIS FORMAT FOR THE BULK INSERT TO WORK,
#   !!! OTHERWISE YOU WILL OPEN THE GATES OF HELL
#   !!! AND BRING UPON THEE MY WRATH
#   each elem in elems has the following structure:
#   * elem[0] = tweet ID - is the PK
#   * elem[1] = raw text of the document
#   * elem[2] = the date of the tweet
#   * elem[3] = author ID of the tweet
#   * elem[4] = language of the tweet, default English
#   * elem[5] = location - coordinates
#   * elem[6] = author age
#   * elem[7] = author gender

# language, default English
# param mode is for the lemmatizer 0 - fast but not accurate, 1 slow but more accurate

documents = []
def results(result):
    if result:
        documents.append(result)

def populateDatabase(elems, language='EN', dbname='TwitterDB', mode=0):
    start = time.time()
    client = pymongo.MongoClient()
    db = client[dbname]
    if elems:

        no_threads = cpu_count()
        pool = ThreadPool(no_threads)
        for elem in elems:
            if len(elem) >= 4:
                # verify if document already in the database
                # only if it does not exist an new document is added to the documents list
                exist = db.documents.find_one(spec_or_id={"_id": str(elem[0])})
                if not exist:
                    pool.apply_async(func = processElement, args=(elem, language, mode), callback=results)
                else:
                    print exist
            else:
                try:
                    print "tweet with problems: ", elem[0]
                except Exception, e:
                    print e
        pool.close()
        pool.join()
        end = time.time()
        print 'text process time', (end - start)
        if documents:
            db.documents.insert(documents)

#process one element
def processElement(elem, language, mode=0):
    document = dict()
    # get language
    if len(elem) >= 5:
        lang = elem[4]
    else:
        lang = language
    # get clean text
    cleanText, hashtags, attags = ct.cleanText(elem[1], lang)
    # if clean text exists
    if len(ct.removePunctuation(cleanText)) > 0:
        # extract lemmas and part of speech
        lemmas = LemmatizeText(rawText=ct.removePunctuation(cleanText), language=lang, mode=mode)
        lemmas.createLemmaText()
        lemmaText = lemmas.cleanText
        if lemmaText and lemmaText != " ":
            lemmas.createLemmas()
            words = []
            for w in lemmas.wordList:
                word = dict()
                word['word'] = w.word
                word['tf'] = w.tf
                word['count'] = w.count
                word['pos'] = w.wtype
                words.append(word)

            # geo location [x, y]
            if len(elem) >= 6:
                document['geoLocation'] = elem[5].split(' ')
            # author age
            if len(elem) >= 7:
                document['age'] = int(elem[6])
            # author gender
            if len(elem) >= 8:
                document['gender'] = elem[7]

            # named entities:
            ner = NamedEntitiesRegonizer(text=cleanText, language=lang)
            ner.createNamedEntities()
            if ner.ner:
                document['namedEntities'] = ner.ner

            # construct the document
            document['_id'] = elem[0]
            document['rawText'] = elem[1]
            document['cleanText'] = cleanText
            document['lemmaText'] = lemmaText
            document['date'] = elem[2]
            document['author'] = elem[3]
            document['words'] = words
            if attags:
                document['attags'] = attags
            if hashtags:
                document['hashtags'] = hashtags
    return document
