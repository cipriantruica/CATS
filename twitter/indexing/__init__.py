# coding: utf-8

__author__ = "Ciprian-Octavian Truica"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

#this is the init file for the indexes
import os
package_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.sys.path.append(package_dir)

__all__ = ['inverted_index', 'pos_index', 'vocabulary_index']

"""
from inverted_index import InvertedIndex
from pos_index import POSIndex
from vocabulary_index import VocabularyIndex


from twitter.indexing.inverted_index import InvertedIndex
from twitter.indexing.pos_index import POSIndex
from twitter.indexing.vocabulary_index import VocabularyIndex
"""