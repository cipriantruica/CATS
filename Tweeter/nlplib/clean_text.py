# coding: utf-8
import sys
import re
import static
import string
import unicodedata
from nltk.corpus import stopwords

reload(sys)  
sys.setdefaultencoding('utf8')

punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
cachedStopWords_en = stopwords.words("english")
cachedStopWords_fr = stopwords.words("french") + ["ce", "cet", "cette", "le", "les"]
contractions_en = static.contractionsEN()
contractions_fr = static.contractionsFR()
contractions_re_en = re.compile('(%s)' % '|'.join(contractions_en.keys()))
contractions_re_fr = re.compile('(%s)' % '|'.join(contractions_fr.keys()))
specialchar_re = re.compile('(%s)' % '|'.join(static.specialchar_dic.keys()))
#remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
remove_punctuation_map = dict((ord(char), None) for char in punctuation)
table = string.maketrans("","")

class CleanText:	
	#remove punctuation, replaces it with space
	def removePunctuation(self, text, language='EN'):
		#return text.translate(remove_punctuation_map)
		#return text.translate(table, punctuation)		
		for c in punctuation:
			text = text.replace(c, ' ')
		return text
		
	#remove scripts from text
	def removeScripts(self, text):
		return re.sub(r"(?is)(<script[^>]*>)(.*?)(</script>)", '', text)

	#removes all tags from an xml file
	# does not keep <img> tag because it is not well formed - TO DO
	def removeTags(self, text):
		return re.sub(re.compile('<.*?>'),'', text)

	#remove any urls from text
	def removeURLs(self, text):
		return re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

	#replace UTF-8 characters with ASCII ones 
	def replaceUTF8Char(self, text, specialchars=static.specialchar_dic):
		def replace(match):			
			return specialchars[match.group(0)]
		return specialchar_re.sub(replace, text)


	#expand contrations
	#only for english
	def expandContractions(self, text, language='EN'):
		def replace(match):
			return contractions_dict[match.group(0)]
		if language == 'EN':
			contractions_dict=contractions_en
			return contractions_re_en.sub(replace, text)
		elif language == 'FR':
			contractions_dict=contractions_fr
			return contractions_re_fr.sub(replace, text)

	#remove stopwords for English and French
	def removeStopWords(self, text, language='EN'):
		text = text.decode("utf8").encode("utf8")
		if language == 'EN':
			return ' '.join([word for word in text.split() if word not in cachedStopWords_en]).encode("utf8")
		elif language == 'FR':			
			return ' '.join([word for word in text.split() if word not in cachedStopWords_fr]).encode("utf8")


	#split string by character
	def splitString(self, str, ch = ',', rch = ''):
		return [e.replace(' ', rch) for e in str.split(ch)]

	#remove multiple spaces from string
	def removeMultipleSpaces(self, text):
		return re.sub(' +',' ',text)

	#function that cleans text
	#depending on the language
	def cleanText(self, text, language = 'EN'):
		text = self.replaceUTF8Char(self.removeURLs(self.removeTags(self.removeScripts(text))))
		text = self.expandContractions(text, language)
		#text = self.removeStopWords(text.lower(), language)
		#text = self.removePunctuation(text)
		return self.removeMultipleSpaces(text.strip())
			