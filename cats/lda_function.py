from gensim import corpora, models

def trainLDA(num_topics=15, num_words=10, iterations=500):
    documents = []
    documentsDB = db.documents.find(query, {'lemmaText': 1, '_id': 0})
    for document in documentsDB:
        documents.append(document['lemmaText'].split())
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(document) for document in documents]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, iterations=iterations, num_topics=15)
    for elem in lda.show_topics(num_topics=num_topics, num_words=num_words, formatted=False):
        print elem

