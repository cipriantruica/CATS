from mllib.train_lda import TrainLDA

lda = TrainLDA(dbname='TwitterDB')
topics = lda.trainLDA(query={'gender': 'femme'})

for t in topics:
    print t