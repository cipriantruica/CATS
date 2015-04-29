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

getCurrentTimeInMili() {
  date +'%H 3600 * %M 60 * + %S + 1000 * %N 1000000 / + p' | dc
}

FILE="../DATA_SETS/tweets/CATS_demo.csv"
DB="ERICDB_tweets"
echo $FILE
for i in `seq 1 $N`
do
	echo "test_$i"
	START=$(getCurrentTimeInMili)
	python testing_tweets.py $FILE $DELIMITER $HEADER $DB $LANGUAGE >> $path"perforance"
	END=$(getCurrentTimeInMili)
	DIFF=$(( $END - $START ))
	echo "*******************" >> $path"perforance"
	echo $DIFF >> $path"100_script_performance"
done;
