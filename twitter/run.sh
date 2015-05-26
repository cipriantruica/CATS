#!/bin/bash

#args:
#1 - file
#2 - delimiter
#3 - has header
#4 - Database name
#example: python populateDB.py DATA_SETS/news_articles/rss.csv t 1 2 ERICDB

N=$1

HEADER=0
DELIMITER="t"
LMTZ=1
OP=1
LANGUAGE=$2
path="times/"
INIT=0
FILE="/home/cats/data/CATS_demo_May-12-2015_3.csv"
DB="TwitterDB2"
echo $FILE
for i in `seq 1 $N`
do
	echo "test_$i"
	python testing_tweets.py $FILE $DELIMITER $HEADER $DB $LANGUAGE $INIT
	echo "*******************" >> $path"perforance"
done;
