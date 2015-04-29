import pymongo

mapFunction = """function() {
			for (var idx=0; idx<this.words.length; idx++){
				var key = this.words[idx].word;
				pos = this.words[idx].wtype;
				var value = { 'pos': pos};
				emit(key, value);
			}
		}"""

reduceFunction = """function(key, values) {
			var result = {'pos': []};
			values.forEach(function (v) {
				result.pos = v.pos.concat(result.pos);
			});
			return result;
		}"""

functionCreate = """function(){
		var items = db.temp_collection.find().addOption(DBQuery.Option.noTimeout);
		while(items.hasNext()){
			var item = items.next();
			pos_uniq = item.value.pos.reduce(function(a,b){
					if (a.indexOf(b) < 0 ) {
						a.push(b);
					}
				return a; },[]);
			doc = {word: item._id, createdAt: new Date(), pos: pos_uniq};
			db.pos_index.insert(doc);
		}		
	}"""

functionUpdate = """function(startDate){
			var items = db.temp_collection.find().addOption(DBQuery.Option.noTimeout);
			while(items.hasNext()){
				var item = items.next();
				var wordID = item._id;
				var pos_uniq = item.value.pos.reduce(function(a,b){
						if (a.indexOf(b) < 0 ) {
							a.push(b);
						}
				return a; },[]);
				var exists = db.pos_index.findOne({word: wordID}, {pos: 1, _id: 0});
				if (exists){
					var pos = exists.pos;
					pos = pos.concat(pos_uniq);
					pos = pos.reduce(function(a,b){
								if (a.indexOf(b) < 0 ) {
									a.push(b);
								}
								return a; },[]);
					db.pos_index.update({word: wordID}, {$set: {pos: pos}});
				}else{
					doc = {word: wordID, createdAt: new Date(), pos: pos_uniq};
					db.pos_index.insert(doc);
				}
			}
	}"""

class POSIndex:
	def __init__(self, dbname):
		client = pymongo.MongoClient()
		self.db = client[dbname]
	
	def createIndex(self, query=None):
		self.db.pos_index.drop()
		if query:
			self.db.words.map_reduce(mapFunction, reduceFunction, "temp_collection", query = query)
		else:
			self.db.words.map_reduce(mapFunction, reduceFunction, "temp_collection")
		self.db.eval(functionCreate)
		self.db.pos_index.ensure_index("word")
		self.db.temp_collection.drop()
	
	#update index after docunemts are added
	def updateIndex(self, startDate):
		query = query = {"createdAt": {"$gt": startDate } }
		self.db.words.map_reduce(mapFunction, reduceFunction, "temp_collection", query = query)
		self.db.eval(functionCreate, {'startDate': startDate})
		self.db.temp_collection.drop()


