import pymongo
from gensim.utils import lemmatize
from nlplib.clean_text import CleanText
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
import time

client = pymongo.MongoClient()
db = client['ERICDB']
cleanText = CleanText()

function = """function(){
				var items = db.search_index2.find().addOption(DBQuery.Option.noTimeout);
				while(items.hasNext()){
				var item = items.next();
					doc = {word: item._id, docIDs: item.value.docIDs};
					db.search_index.insert(doc);
				}
			}"""

mapFunction = """function() {
				var key = this.word;
				for (var idx=0; idx<this.docIDs.length; idx++){
					var tfidf = this.idf * this.docIDs[idx].tf;
					value = { 'docID': this.docIDs[idx].docID, 'TFIDF': tfidf };
					emit(key, {'docIDs': [value]});
				}
			}"""

reduceFunction = """function(key, values){
				var result = {'docIDs': []};
				values.forEach(function(v){
					result.docIDs = v.docIDs.concat(result.docIDs);
				});
				return result;
			}"""

class Search:
	def score(self, word):

		db.vocabulary.map_reduce(mapFunction, reduceFunction, 'search_index2', query={'word': word})
		db.eval(function)
		response = db.search_index.find({'word': word}, {'docIDs': 1, '_id': 0})
		lista = {}
		for value in response[0]['docIDs']:
			lista[value['docID']] = value['TFIDF']
		db.search_index2.drop()
		db.search_index2.drop()
		return lista

	def rank(self, searchPhrase):
		keys = []
		scorePhrase = {}
		for word in searchPhrase:
			if not keys:				
				keys = self.listSearch[word].keys()
			else:
				keys = list(set(keys) & set(self.listSearch[word].keys()))
		for key in keys:
			score = 0
			for word in searchPhrase:
				score += self.listSearch[word][key]
			scorePhrase[key] = round(score, 2)
		#print searchPhrase, scorePhrase
		return scorePhrase, keys
				
	def subQueries(self, searchPhrase):
		words = [word.split('/')[0] for word in lemmatize(cleanText.removeStopWords(cleanText.cleanText(searchPhrase)))]
		searchWords = []
		for L in range(len(words) + 1, 0, -1):
			for subset in combinations(words, L):
				searchWords.append(list(subset))
		return words, searchWords

	def __init__(self, searchPhrase, k):
		words, subSearch = self.subQueries(searchPhrase)
		self.listSearch = {}
		no_threads = cpu_count()

		with ThreadPoolExecutor(max_workers = no_threads) as e:
			for word in words:
				result = e.submit(self.score, word)
				self.listSearch[word] = result.result()

		keys = {}
		rankedPhrase = {}
		
		with ThreadPoolExecutor(max_workers = no_threads) as e:
			for phrase in subSearch:
				result = e.submit(self.rank, phrase)
				rankedPhrase[' '.join(word for word in phrase)], keys[' '.join(word for word in phrase)] = result.result()
		"""
		for phrase in subSearch:
			rankedPhrase[' '.join(word for word in phrase)], keys[' '.join(word for word in phrase)] = self.rank(phrase)
		"""
		
		distinctKeys = []
		for key in keys:			
			distinctKeys += keys[key]
		distinctKeys =list(set(distinctKeys))


		answer = {}
		for key in distinctKeys:
			for phrase in subSearch:
				if rankedPhrase[' '.join(word for word in phrase)].get(key, -1) != -1:
					answer[key] = max(rankedPhrase[' '.join(word for word in phrase)][key], answer.get(key, -1))

		#print answer.values()
		answer = sorted(answer.items(), key=lambda x: x[1], reverse=True)
		
		idx = 0
		for key in answer:
			#print key
			idx += 1
			if idx == k:
				break



if __name__ == "__main__":
	db.search_index.drop()
	searchPhrase = []
	searchPhrase.append("absurd")
	searchPhrase.append("absurd ability")
	searchPhrase.append("absurd ability action")
	searchPhrase.append("absurd ability action back")
	searchPhrase.append("absurd ability action back go")
	for i in range(0,5):
		time_words = []
		for j in range(0, 5):
			start = time.time()
			search = Search(searchPhrase[i], 20)
			end = time.time() 
			time_words.append(end-start)
		print "no search words:", i+1, " k = ", 20, 'mean time:', round(sum(time_words)/len(time_words), 2)
