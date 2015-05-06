# coding: utf-8
from vocabulary_index import VocabularyIndex

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2014, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

query = {"word.words" : {"$in":["curry","cara","cuti"]} "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
#"author" : "76570268", 
vocab = VocabularyIndex('TwitterDB')
vocab.createIndex(query=query)