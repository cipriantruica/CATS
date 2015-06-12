# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@ca.pub.ro"
__status__ = "Production"

#this is the init file for the ml lib
import os
package_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print package_dir
os.sys.path.append(package_dir)

__all__ = ['market_matrix', 'topic_modeling']

"""
from market_matrix import MarketMatrix
from topic_modeling import TopicModeling


from cats.mllib.market_matrix import MarketMatrix
from cats.mllib.topic_modeling import TopicModeling
"""
