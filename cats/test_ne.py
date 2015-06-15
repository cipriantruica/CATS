__author__ = 'sheepman'

import pymongo

if __name__ == '__main__':
    client = pymongo.MongoClient()
    dbname = 'TwitterDB'
    db = client[dbname]
    #TO DO see how to use exists!!!!
    # query_or = {"words.word" : {"$in": ["shit", "fuck"] }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}, 'namedEntities': {'$exists': 'true'}}
    query_or = {'namedEntities': {'$exists': 'true'}}
    cursor = db.documents.find(spec=query_or, fields={'namedEntities': 1, '_id': 0})
    # namedEntitiesDict = dict()
    # namedEntitiesDict = {'ORGANIZATION': {}, 'PERSON': {}, 'LOCATION': {}}
    # for elem in cursor:
    #     for ne in elem['namedEntities']:
    #         if ne['type'] == 'ORGANIZATION':
    #             if namedEntitiesDict['ORGANIZATION'].get(ne['entity']):
    #                 namedEntitiesDict['ORGANIZATION'][ne['entity']] += 1
    #             else:
    #                 namedEntitiesDict['ORGANIZATION'][ne['entity']] = 1
    #         if ne['type'] == 'PERSON':
    #             if namedEntitiesDict['PERSON'].get(ne['entity']):
    #                 namedEntitiesDict['PERSON'][ne['entity']] += 1
    #             else:
    #                 namedEntitiesDict['PERSON'][ne['entity']] = 1
    #
    #         if ne['type'] == 'LOCATION':
    #             if namedEntitiesDict['LOCATION'].get(ne['entity']):
    #                 namedEntitiesDict['LOCATION'][ne['entity']] += 1
    #             else:
    #                 namedEntitiesDict['LOCATION'][ne['entity']] = 1
    #
    # for key, value in namedEntitiesDict.items():
    #     if value:
    #         # print key, value
    #         for ne, count in value.items():
    #             print ne, count, key
    # cursor.rewind()


    print 'test2'
    namedEntitiesDict2 = list()
    for elem in cursor:
        for ne in elem['namedEntities']:
            if ne['type'] != 'GPE':
                ok = True
                for elem in namedEntitiesDict2:
                    if elem['entity'] == ne['entity']:
                        ok = False
                        elem['count'] += 1
                        break
                if ok:
                    namedEntitiesDict2.append({'entity': ne['entity'], 'count': 1, 'type': ne['type']})



    for elem in namedEntitiesDict2:
        print elem['entity'], elem['count'], elem['type']


