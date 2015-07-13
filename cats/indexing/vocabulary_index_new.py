# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
from time import time

mapFunction = """function() {
                    for (var idx=0; idx<this.words.length; idx++){
                        var key = this.words[idx].word;
                        var values = {
                            tf: this.words[idx].tf,
                            count: 1
                        };
                        emit(key, values);
                    }
                }"""

reduceFunction = """function(key, values) {
                        var result = {tf: 0, count: 0};
                        for(var idx = 0; idx < values.length; idx++){
                            result.count += values[idx].count;
                            result.tf += values[idx].tf;
                        };
                        return result;
                    }"""

functionCreate = """function(){
                        var noDocs = db.documents.count();
                        var items = db.temp_collection.find().addOption(DBQuery.Option.noTimeout);
                        while(items.hasNext()){
                            var item = items.next();
                            var idf = 1 + Math.round(Math.log(noDocs/item.value.count) * 100)/100;
                            var tfidf = Math.round(idf * item.value.tf * 100)/100;
                            doc = {word: item._id, IDF: idf, TFIDF: tfidf};
                            db.vocabulary.insert(doc);
                        }
                        db.vocabulary.ensureIndex({IDF:1});
                        db.temp_collection.drop();
                    }"""

functionCreateQuery = """function(query){
                        var noDocs = db.documents.count(query);
                        var items = db.temp_collection.find().addOption(DBQuery.Option.noTimeout);
                        while(items.hasNext()){
                            var item = items.next();
                            var idf = 1 + Math.round(Math.log(noDocs/item.value.count) * 100)/100;
                            var tfidf = Math.round(idf * item.value.tf * 100)/100;
                            doc = {word: item._id, IDF: idf, TFIDF: tfidf};
                            db.vocabulary.insert(doc);
                        }
                        db.vocabulary_query.ensureIndex({'idf':1});
                        db.temp_collection.drop();
                    }"""



class VocabularyIndex:
    def __init__(self, dbname):
        client = pymongo.MongoClient()
        self.db = client[dbname]
        self.db.documents.ensure_index([('words.word', pymongo.ASCENDING)])
    
    def createIndex(self, query=None):
        if query:
            self.db.vocabulary_query.drop()
            self.db.documents.map_reduce(mapFunction, reduceFunction, "temp_collection", query=query, sort={'words.word': 1})
            self.db.eval(functionCreateQuery, query)
        else:
            self.db.vocabulary.drop()
            self.db.documents.map_reduce(mapFunction, reduceFunction, "temp_collection", sort={'words.word': 1})
            self.db.eval(functionCreate)


if __name__ == '__main__':
    print "Starting..."
    query = dict()
    query['gender'] = 'homme'
    query["words.word"] = {"$in": ['cat', 'dog'] }
    print "Starting initializing class..."
    start = time()
    vi = VocabularyIndex(dbname='TwitterDB_test')
    end = time()
    print "time:", (end-start)
    print "Starting Create Index without query..."
    start = time()
    vi.createIndex()
    end = time()
    print "time:", (end-start)
    print "Starting Create Index with query...", query
    start = time()
    vi.createIndex(query=query)
    end = time()
    print "time:", (end-start)

    # testing for OLAPDB
    # query['authors.genderid'] = 1
    # query["words.word"] = {"$in": ['cat', 'dog'] }
    # print "Starting initializing class..."
    # start = time()
    # vi = VocabularyIndex(dbname='OLAPDB')
    # end = time()
    # print "time:", (end-start)
    # print "Starting Create Index without query..."
    # start = time()
    # vi.createIndex(query={})
    # end = time()
    # print "time:", (end-start)
    # print "Starting Create Index with query...", query
    # start = time()
    # vi.createIndex(query=query)
    # end = time()
    # print "time:", (end-start)