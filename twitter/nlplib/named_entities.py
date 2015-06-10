# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import nltk

#TO DO try this for french
class NamedEntitiesRegonizer:
    def __init__(self, text, language='EN'):
        self.ner = []
        self.gpe = []
        self.person = []
        self.organization = []
        self.facility = []
        self.location = []
        self.text = text
        self.language = language

    def createNamedEntities(self):
        #only for English for now :)
        try:
            if self.language == 'EN':
                sentences = nltk.sent_tokenize(self.text)
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
        except Exception as e:
            print self.text, '\n', e

#this is just a test using tweets
if __name__ == '__main__':
    texts = [
        "Arg & Lydia ??????",
        "Claire is constant overreactions to her baby going missing are so annoying.",
        "Christ knows. Been out myself, just come home and it stinks all over. No ones in. Hate cig smells.",
        "Nathan could you tweet happy birthday to it would make her day! She was at Bundoran today :)",
        "I liked a video from Wiz Khalifa - See You Again ft. Charlie Puth [Official Video]",
        "I was rly close with Leo, I never rly spoke to Charlie bc he was studying all the time for gcses??",
        "charlie I no u will not see this and I no it is so cheesy but I love u so much",
        "Wiz Khalifa - See You Again ft. Charlie Puth [Official Video] Furious 7 Soundtrack. Emotional",
        "Everyone was like \\who the fuck is Charlie\\\" mate use yo brains\"",
        "Happy birthday Cardiff Charlie!! Have a good one darling One love????",
        "Charlie Mulgrew has the most beautiful family ever",
        "Telling that Averil Power, and not. Charlie McConalogue is acting as FF spokesperson for education on tonight. She is much better."
    ]

    for text in texts:
        print text
        ner = NamedEntitiesRegonizer(text=text)
        ner.createNamedEntities()
        print "person:", ner.person
        print "organization:", ner.organization
        print "gpe:", ner.gpe
        print "facility:", ner.facility
        print "location:", ner.location