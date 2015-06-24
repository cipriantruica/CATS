# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
import codecs
from datetime import datetime

class MabedFiles:
    def __init__(self, dbname='TwitterDB'):
        client = pymongo.MongoClient()
        self.db = client[dbname]

    def buildFiles(self, query={}, slice=30, filename='mabed'):
        try:
            # get date
            if query and query.get("date"):
                startDate =  datetime.strptime(query["date"]["$gt"] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                endDate = datetime.strptime(query["date"]["$lte"] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
            else:
                startDate = datetime.strptime(self.db.documents.find(spec=query, fields={'date': 1, '_id': 0}, limit=1, sort=[('date',pymongo.ASCENDING)])[0]['date'], '%Y-%m-%d %H:%M:%S')
                endDate = datetime.strptime(self.db.documents.find(spec=query, fields={'date': 1, '_id': 0}, limit=1, sort=[('date',pymongo.DESCENDING)])[0]['date'], '%Y-%m-%d %H:%M:%S')
            print slice, startDate, endDate
            # documents = self.db.documents.find(spec=query, fields={'rawText': 1, 'date': 1, '_id': 0})
            # with codecs.open(filename+'.text', "w", "utf-8") as textfile, codecs.open(filename+'.time', "w", "utf-8") as timefile:
            #     for elem in documents:
            #         # encode string to UTF-8
            #         # encode Escape character so that they can be removed
            #         # remove carriage return and new line
            #         text = elem['rawText'].encode('utf8').encode('string_escape').replace('\r', '').replace('\n', '')
            #         textfile.write(text + '\n')
            #         timefile.write(elem['date']+'\n')
        except Exception as e:
            print e

if __name__ == '__main__':
    mf = MabedFiles(dbname='TwitterDB')
    query1 = {'words.word': {'$in': [u'fuck']}}
    query2 = {'date': {'$lte': u'2015-04-10', '$gt': u'2015-04-08'}}
    query3 = {'gender': u'femme', 'age': {'$in': [u'5-11', u'12-18', u'45-60', u'61-99']}, 'words.word': {'$in': [u'fuck']}}
    query4 = {}
    mf.buildFiles(slice=0)
    mf.buildFiles(query1, slice=1)
    mf.buildFiles(query2, slice=2)
    mf.buildFiles(query3, slice=3)
    mf.buildFiles(query4, slice=4)



