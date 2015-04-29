# coding: utf-8
from __future__ import division
from gensim.utils import lemmatize
from nlplib.clean_text import CleanText
from nltk.corpus import wordnet
from nltk.tag.stanford import POSTagger
from pattern.fr import parse as parseFR
from pattern.en import parse as parseEN
from nltk.corpus import stopwords

#TO_DO modify this class to accept french also
class LemmatizeText:
	class Word():
		word = ""
		wtype = []
		count = 0
		tf = 0.0

	def __init__(self, rawText, language='EN'):
		self.wordList = []
		self.rawText = rawText
		self.cleanText = ""	
		self.words = []
		self.language = language

	def createLemmaText(self):
		ct = CleanText()
		if self.language == 'EN':
			"""
			lemmas = lemmatize(ct.removeStopWords(self.rawText))
			for word in lemmas:
				elems = word.split('/')
				self.words.append((elems[0], elems[1]))
			self.cleanText = ' '.join(word[0] for word in self.words)
			"""
			text = self.rawText
			text = text.lower()
			text = ct.removeStopWords(text, self.language)
			text = ct.removePunctuation(text)
			text = parseEN(text, tags = False, chunks = False, lemmata=True).split()
			#print text
			try:
				for word in text[0]:
					self.words.append((word[2], word[1][:2]))
				self.cleanText = ' '.join(word[0] for word in self.words)
			except Exception as e:
				print e, self.rawText
		if self.language == 'FR':
			text = self.rawText
			text = text.lower()
			text = ct.removeStopWords(text, self.language)
			text= ct.removePunctuation(text)	
			text = parseFR(text, tags = False, chunks = False, lemmata=True).split()
			for word in text[0]:
				#if word[2] 	not in stopwords.words("french"):
				if word[1][:2] in ['RB', 'NN', 'VB', 'JJ']:
					self.words.append((word[2], word[1][:2]))
			self.cleanText = ' '.join(word[0] for word in self.words)


	def createLemmas(self):
		if self.cleanText:
			for word in self.words:
				self.append(word[0], word[1])
			#sort wordList by word count
			self.wordList = sorted(self.wordList, key=lambda word: word.count)
			#calculate TF
			maxF = self.wordList[-1].count
			for idx in xrange(0,len(self.wordList), 1):
				self.wordList[idx].tf = round(0.5 + (0.5 * self.wordList[idx].count)/maxF, 2)

	def append(self, word, wtype):
		if word:
			if not self.wordList:
				newWord = self.Word()
				newWord.count = 1
				newWord.word = word
				newWord.wtype = []
				newWord.wtype.append(wtype)
				self.wordList.append(newWord)
			else:
				notInList = True
				for idx in xrange(0,len(self.wordList), 1):
					if word == self.wordList[idx].word:
						if wtype not in self.wordList[idx].wtype:
							self.wordList[idx].wtype.append(wtype)
						self.wordList[idx].count += 1
						notInList = False
						break

				if notInList:
					newWord = self.Word()
					newWord.count = 1
					newWord.word = word
					newWord.wtype = []
					newWord.wtype.append(wtype)
					self.wordList.append(newWord)
	#testing
	def printList(self):
		for words in self.wordList:
			print words.word, "pos", words.wtype, "count:", words.count, "TF:", words.tf
