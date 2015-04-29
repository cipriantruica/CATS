import csv

#author field parse
def getAuthorName(text, ch = ','):
	return [(' '.join(name.split(' ')[:-1]), name.split(' ')[-1]) for name in text.split(ch)]

#this part is for reading the file

def determineDelimiter(character):	
	if character == 't':
		return '\t'
	elif character == 'c':
		return ','
	elif character == 's':
		return ';'

def readCSV(filename, csv_delimiter = ';', header = True):	
	with open(filename, 'rU') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = csv_delimiter)		
		if header:	#the csv file contain a header
			h = spamreader.next()
			return h, [row for row in spamreader]
		else:
			return [], [row for row in spamreader]