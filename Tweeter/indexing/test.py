from vocabulary_index import VocabularyIndex

query = {"word.words" : {"$in":["curry","cara","cuti"]} "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
#"author" : "76570268", 
vocab = VocabularyIndex('TwitterDB')
vocab.createIndex(query=query)