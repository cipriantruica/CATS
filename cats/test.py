from mllib.train_lda import TrainLDA
from mllib.topic_modeling import TopicModeling
from mllib.market_matrix import MarketMatrix
from indexing.vocabulary_index import VocabularyIndex
from time import time

print 'Using TrainLDA class... \n'
start = time()
lda = TrainLDA(dbname='TwitterDB')
topics = lda.trainLDA(query={'gender': 'homme'}, num_topics=15, num_words=10, iterations=500)
for t in topics:
    print t, '\n'

end = time()
print 'total time', (end - start)
print '\n\n================================================\n\n'

vocab = VocabularyIndex(dbname='TwitterDB')
vocab.createIndex(query={'gender': 'homme'})

print 'Using MM and TopicModeling classes... \n'
start = time()
mm = MarketMatrix(dbname='TwitterDB')
mm.build(query=True)
id2word, id2tweetID, market_matrix = mm.buildTFIDFMM()

tp = TopicModeling(id2word=id2word, corpus=market_matrix)
tops = tp.topicsLDA(num_topics=15, num_iterations=500, num_words=10)

for t in tops:
    print t, '\n'
end = time()
print 'total time', (end - start)

print '\n\n================================================\n\n'
