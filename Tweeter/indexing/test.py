from vocabulary_index import VocabularyIndex

query = {"author" : "76570268", "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}

vocab = VocabularyIndex('TwitterDB')
vocab.createIndex(query=query)