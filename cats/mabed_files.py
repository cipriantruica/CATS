# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
import codecs

class MabedFiles:
    def __init__(self, dbname='TwitterDB'):
        client = pymongo.MongoClient()
        self.db = client[dbname]

    def buildFiles(self, query={}, filename='mabed'):
        try:
            documents = self.db.documents.find(query, {'rawText': 1, 'date': 1, '_id': 0})
            with codecs.open(filename+'.text', "w", "utf-8") as textfile, codecs.open(filename+'.time', "w", "utf-8") as timefile:
                for elem in documents:
                    # encode string to UTF-8
                    # encode Escape character so that they can be removed
                    # remove carriage return and new line
                    text = elem['rawText'].encode('utf8').encode('string_escape').replace('\r', '').replace('\n', '')
                    textfile.write(text + '\n')
                    timefile.write(elem['date']+'\n')
        except Exception as e:
            print e

if __name__ == '__main__':
    mf = MabedFiles(dbname='TwitterDB')
    mf.buildFiles()



