__author__ = "Adrien Guille"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "adrien.guille@univ-lyon2.fr"
__status__ = "Production"

from twitter import *
import datetime

tweets_per_file = 5

def quote(string):
    return '"'+string.encode('utf-8')+'"'

def collect_tweets(keywords):
    nb_tweets = 0
    nb_tweets_infile = 0
    nb_files = 1
    file = open(str(nb_files)+'.csv', 'a')
    print(open('consumer_key','r').read())
    print(open('consumer_secret','r').read())
    print(open('token','r').read())
    print(open('token_secret','r').read())
    auth = OAuth(
        consumer_key=str(open('consumer_key','r').read()),
        consumer_secret=str(open('consumer_secret','r').read()),
        token=str(open('token','r').read()),
        token_secret=str(open('token_secret','r').read())
    )
    twitter_stream = TwitterStream(auth=auth)
    iterator = twitter_stream.statuses.filter(track=keywords)
    for tweet in iterator:
        if tweet.get('text'):
            text = tweet['text']
            text = text.replace('"',' ')
            text = quote(text.replace('\n',' '))
            geo = ''
            if(tweet.get('geo')):
                geo = tweet['geo']
            geo = quote(geo)    
            timestamp = quote(datetime.datetime.fromtimestamp(float(tweet['timestamp_ms'])/1000).strftime('%Y-%m-%d %H:%M:%S'))  
            nb_tweets += 1
            nb_tweets_infile += 1
            description = ''
            if(tweet['user'].get('description')):
                description = tweet['user']['description']
                description = description.replace('"',' ')
                description = description.replace('\n',' ')
            description = quote(description)
            name = ''
            if(tweet['user'].get('name')):
                name = tweet['user']['name']
            name = quote(name)
            file.write(quote(str(tweet['id']))+'\t'+text+'\t'+timestamp+'\t'+quote(str(tweet['user']['id']))+'\t'+geo+'\t'+description+'\t'+name+'\t'+quote(tweet['lang'])+'\n')
            if(nb_tweets_infile == tweets_per_file):
                nb_files += 1
                nb_tweets_infile = 0
                file = open(str(nb_files)+'.csv', 'a')
        
collect_tweets('obama')