__author__ = "Adrien Guille"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "adrien.guille@univ-lyon2.fr"
__status__ = "Production"

from twitter import *
import datetime
import threading
import subprocess

tweets_per_file = 1000

def quote(string):
    return '"'+string.encode('utf-8')+'"'

class Streaming:
    def __init__(self, dbname='TwitterDBTest'):
        print '__init__ Streaming...'
        db_name = dbname

    def threadUpdate(self,filename):
        print('Importing',filename,'...')
        filepath = 'data/'+str(filename)+'.csv'
        subprocess.call(['sh','update.sh',self.db_name,filepath])
        print('Done.')

    def collect_tweets(self,duration=1,keywords=None,users=None,locations=None):
        nb_tweets = 0
        nb_tweets_infile = 0
        nb_files = 1
        lock = open("collection.lock", "w")
        lock.write(" ")
        lock.close()
        file = open('data/'+str(nb_files)+'.csv', 'a')
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
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=int(duration))
        if keywords is not None:
            print("keywords")
            iterator = twitter_stream.statuses.filter(track=keywords)
        elif users is not None:
            print("users")
            iterator = twitter_stream.statuses.filter(follow=users)
        else:
            iterator = twitter_stream.statuses.filter(locations=location)
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
                    current_date = datetime.datetime.today()
                    if current_date <= end_date:
                        t = threading.Thread(target=threadUpdate, args=(nb_files,))
                        t.start()
                        nb_files += 1
                        nb_tweets_infile = 0
                        file = open('data/'+str(nb_files)+'.csv', 'a')
                    else:
                        break

                    
if __name__ == '__main__':
    s = Streaming(dbname='TwitterDBTest')
    keywords = 'obama,hollande'
    users = '7302282,14857290,133663801'
    location = '-122.75,36.8,-121.75,37.8'
    s.collect_tweets(keywords=keywords)