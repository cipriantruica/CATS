import nltk

#TO DO try this for french
class NamedEntitiesRegonizer:
	def __init__(self, document):
		self.ner = []
		self.gpe = []
		self.person = []
		self.organization = []
		self.facility = []
		self.location = []
		self.document = document

	def createNamedEntities(self):
		sentences = nltk.sent_tokenize(self.document)
		sentences = [nltk.word_tokenize(sent) for sent in sentences]
		sentences = [nltk.pos_tag(sent) for sent in sentences]
		sentences = [nltk.ne_chunk(sent) for sent in sentences]
		for tree in sentences:
			self.ner += [(ne.label(), ' '.join(map(lambda x: x[0], ne.leaves()))) for ne in tree if isinstance(ne, nltk.tree.Tree)]
		for elem in self.ner:
			if elem[0] == "PERSON":
				self.person.append(elem[1])
			elif elem[0] == "GPE":
				self.gpe.append(elem[1])
			elif elem[0] == "ORGANIZATION":
				self.organization.append(elem[1])
			elif elem[0] == "FACILITY":
				self.facility.append(elem[1])
			elif elem[0] == "LOCATION":
				self.location.append(elem[1])
		#remove duplicates
		self.person = list(set(self.person))
		self.gpe = list(set(self.gpe))
		self.organization = list(set(self.organization))
		self.facility = list(set(self.facility))
		self.location = list(set(self.location))
