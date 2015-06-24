from mllib.train_lda import TrainLDA

lda = TrainLDA(dbname='TwitterDB')
topics = lda.trainLDA(query={'gender': 'homme'})

for t in topics:
    print t
