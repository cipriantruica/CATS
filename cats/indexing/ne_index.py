# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo

mapFunction = """function(){
                    for (var idx=0; idx<this.namedEntities.length; idx++) {
                        var key = this.namedEntities[idx];
                        var value = {'count': 1};
                        emit(key, value);
                    }
                }"""

reduceFunction = """function(key, value){
                        result = {'count': 0};
                        for (var idx=0; idx<value.length; idx++) {
                            result.count += value[idx].count;
                        }
                        return result;
                    }"""

# db.documents.mapReduce(mapFunction, reduceFunction, {out: "map_reduce_ner", query : {namedEntities: {$exists: true}}})


functionCreate = """function(){
                        db.named_entities.drop();
                        var items = db.map_reduce_ner.find().addOption(DBQuery.Option.noTimeout);
                        documents = Array();
                        while(items.hasNext()){
                            var item = items.next();
                            document = {entity: item._id.entity, type: item._id.type, count: item.value.count};
                            documents.push(document);
                        }
                        db.named_entities.insert(documents);
                        db.map_reduce_ner.drop();
                    }"""

class NEIndex:
    def __init__(self, dbname):
        client = pymongo.MongoClient()
        self.db = client[dbname]

    def createIndex(self, query = None):
        self.db.named_entities.drop()
        if query:
            self.db.documents.map_reduce(mapFunction, reduceFunction, "map_reduce_ner", query = query)
        else:
            self.db.documents.map_reduce(mapFunction, reduceFunction, "map_reduce_ner")
        self.db.eval(functionCreate)