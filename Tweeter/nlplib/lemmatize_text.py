# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

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
		text = self.rawText
		text = text.lower()
		text = ct.removeStopWords(text, self.language)
		text = ct.removePunctuation(text)
		if self.language == 'EN':
			text = parseEN(text, tags = False, chunks = False, lemmata=True).split()
		elif self.language == 'FR':
			text = parseFR(text, tags = False, chunks = False, lemmata=True).split()
		try:
			if text:
				for word in text[0]:
					self.words.append((word[2].lower(), word[1][:2]))
				self.cleanText = ' '.join(word[0] for word in self.words)
		except Exception as e:
			print e, self.rawText


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
