# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

#this is the init file for the project
__all__ = ['inverting', 'mllib', 'nlplib', 'models']

# import os
# package_dir = os.path.abspath(os.path.dirname(__file__))
# os.sys.path.append(package_dir)
#
# for package in __all__:
#     package_dir = os.path.abspath(os.path.dirname(__file__)) + "/" + package
#     os.sys.path.append(package_dir)
#
import sys
print 'cats init'
for elem in  sorted(sys.path):
    print elem
#
#
# import indexing
# import nlplib
# import mllib
# import models

"""
import cats.indexing.vocabulary_index
import cats.nlplib.clean_text
import cats.nlplib.lemmatize_text
import cats.nlplib.named_entities
import cats.mllib.market_matrix
import cats.mllib.topic_modeling
import cats.models.mongo_models
"""