# http://docs.tweepy.org/en/v3.8.0/streaming_how_to.html

# Streaming With Tweepy

# In Tweepy, an instance of tweepy.Stream establishes a streaming session and routes messages to StreamListener instance. 
# The on_data method of a stream listener receives all messages and calls functions according to the message type. 
# The default StreamListener can classify most common twitter messages and routes them to appropriately named methods, 
# but these methods are only stubs.

#author: Prof Lim Tong Ming
#date: 25 Nov 2020
#program: crawler_twitter_keywords.py

# it uses keywords.txt as the tags in your current directory.
# to run: python3 crawler_twitter_keywords.py keywords.txt
# where keywords.txt has a list of your keywords

import tweepy
import time
import csv
import sys
from datetime import datetime
from os.path import join

Gtwitterfilename=" "
Gcsvfile=" "

def start_csv(csvfilename):
    global Gtwitterfilename
    global Gcsvfile
    csvfile=open(csvfilename, 'w', newline='', encoding="utf-8")    
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['id', 'user', 'created_at', 'text', 'source_url', 'truncated', 'source', 'author', 
                        'contributors', 'coordinates', 'destroy', 'entities', 'favorite', 'favorite_count', 
                        'favorited', 'geo', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id', 
                        'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'is_quote_status',
                        'lang', 'parse, parse_list', 'place', 'retweet', 'retweet_count', 'retweeted'])
    Gtwitterfilename=csvfilename
    print("*1* Gtwitterfilename=",Gtwitterfilename," twitterfilename=",csvfilename," **")
    return {'csvwriter':csvwriter, 'csvfile':csvfile}
def append_csv(csvfilename):
    csvfile=open(csvfilename, 'a+', newline='', encoding="utf-8")    
    csvwriter = csv.writer(csvfile)
    return {'csvwriter':csvwriter, 'csvfile':csvfile}
def write_csv(csvwriter, id, user, created_at, text, source_url, truncated, source, author, 
              contributors, coordinates,destroy,entities,favorite,favorite_count, favorited, geo, 
              id_str, in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_status_id_str, 
              in_reply_to_user_id, in_reply_to_user_id_str, is_quote_status, lang, parse, parse_list, 
                        place, retweet, retweet_count, retweeted):
    global Gtwitterfilename
    csvwriter.writerow([id, user, created_at, text, source_url, truncated, source, author, 
                        contributors, coordinates,destroy,entities,favorite,favorite_count, favorited, geo, 
                        id_str, in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_status_id_str, 
                        in_reply_to_user_id, in_reply_to_user_id_str, is_quote_status, lang, parse, parse_list, 
                        place, retweet, retweet_count, retweeted]
                      )
    print("*2* Gtwitterfilename=",Gtwitterfilename," **")
    return
def end_csv(csvfile):
    print("Closing "+Gtwitterfilename)
    print("*3* Gtwitterfilename=",Gtwitterfilename," **")
    csvfile.close()
    return

def createfilename(dirly):
    global Gtwitterfilename
    anow = datetime.now()
    adatetime = anow.strftime("%m%d%Y_%H%M%S")
    Gtwitterfilename = dirly+"twitterKeywords_"+adatetime+".csv"    
    print(Gtwitterfilename, " newly created.")
    print("*4* Gtwitterfilename=",Gtwitterfilename," **")
    return Gtwitterfilename

#'author',
#'contributors',
#'coordinates',
#'created_at',
#'destroy',
#'entities',
#'favorite',
#'favorite_count',
#'favorited',
#'geo',
#'id',
#'id_str',
#'in_reply_to_screen_name',
#'in_reply_to_status_id',
#'in_reply_to_status_id_str',
#'in_reply_to_user_id',
#'in_reply_to_user_id_str',
#'is_quote_status',
#'lang',
#'parse',
#'parse_list',
#'place',
#'retweet',
#'retweet_count',
#'retweeted',
#'retweets',
#'source',
#'source_url',
#'text',
#'truncated',
#'user'

def open_emotionseeds(dirly,filename):
    emotionseed_list=[]
    f = open(dirly+filename, "r")
    for ff in f:
        ff=ff.replace("\n","")
        emotionseed_list.append(ff)
        emotionseed_list.append("#"+ff)
        print(ff)
    f.close()
    print("Closing ",dirly+filename)
    return emotionseed_list

#override tweepy.StreamListener to add logic to on_status
from datetime import datetime
class MyStreamListener(tweepy.StreamListener):

    def __init__(self, num_tweets_to_grab, sleeping_time, twitterfilename, csvwriter, csvfile):
        super(MyStreamListener, self).__init__()
        global Gtwitterfilename
        global Gcsvfile
        self.counter = 0
        self.runno = 1
        self.twitterfilename = twitterfilename
        Gtwitterfilename=self.twitterfilename
        self.csvwriter = csvwriter
        self.csvfile = csvfile
        Gcsvfile=self.csvfile
        self.num_tweets_to_grab = num_tweets_to_grab
        self.sleeping_time = sleeping_time
        print("init counter=",self.counter,
              "\ntwitterfilename=",self.twitterfilename,
              "\ncsvwriter=",self.csvwriter,
              "\ncsvfile=",self.csvfile,
              "\nnum tweets to grab=",self.num_tweets_to_grab,"\n\n")
        print("*5* Gtwitterfilename=",Gtwitterfilename," twitterfilename=",self.twitterfilename," **")

    def on_status(self, status):
        print ("runno=",self.runno)
        print ("counter=",self.counter)

        print ("id=",status.id)
        print ("text",status.text.encode("utf-8"))
        print ("created_at=",status.created_at)
        print ("user=",str(status.user)[:20]+"....."+str(status.user)[len(str(status.user))-20:])
        print ("truncated=",status.truncated)
        print ("source_url=",status.source_url)
        print ("source=",status.source)
        print ("author=",str(status.author)[:20]+"....."+str(status.author)[len(str(status.author))-20:])
        print ("contributors=",status.contributors)
        print ("coordinates=",status.coordinates)        
        print ("destroy=",str(status.destroy)[:20]+"....."+str(status.destroy)[len(str(status.destroy))-20:])
        print ("entities=",status.entities)
        print ("favorite=",str(status.favorite)[:20]+"....."+str(status.favorite)[len(str(status.favorite))-20:])
        print ("favorite_count=",status.favorite_count)
        print ("favorited=",status.favorited)
        print ("geo=",status.geo)
        print ("id_str=",status.id_str)
        print ("in_reply_to_screen_name=",status.in_reply_to_screen_name)
        print ("in_reply_to_status_id=",status.in_reply_to_status_id)
        print ("in_reply_to_status_id_str=",status.in_reply_to_status_id_str)
        print ("in_reply_to_user_id=",status.in_reply_to_user_id)
        print ("in_reply_to_user_id_str=",status.in_reply_to_user_id_str)
        print ("is_quote_status=",status.is_quote_status)
        print ("lang=",status.lang)
        print ("parse=",status.parse)
        print ("parse_list=",status.parse_list)
        print ("place=",status.place)
        print ("retweet=",str(status.retweet)[:20]+"....."+str(status.retweet)[len(str(status.retweet))-20:])
        print ("retweet_count=",status.retweet_count)
        print ("retweeted=",status.retweeted)        
        
        print ("writing to csv..")
        write_csv(self.csvwriter, "'"+str(status.id)+"'", status.user, status.created_at, status.text.encode("utf-8"), 
                  status.source_url, status.truncated, status.source, status.author,status.contributors,
                  status.coordinates,status.destroy,status.entities,status.favorite,status.favorite_count,
                  status.favorited,status.geo,status.id_str,status.in_reply_to_screen_name,status.in_reply_to_status_id,
                  status.in_reply_to_status_id_str,status.in_reply_to_user_id,status.in_reply_to_user_id_str,
                  status.is_quote_status,status.lang,status.parse,status.parse_list,status.place,status.retweet,
                  status.retweet_count,status.retweeted
                 )
        print ("wrtten to csv\n\n")
        self.counter += 1
        self.runno += 1
        global Gtwitterfilename
        global Gcsvfile
        print("*6* Gtwitterfilename=", Gtwitterfilename, " twitterfilename=", self.twitterfilename, " **")
        if self.counter == self.num_tweets_to_grab:
            self.counter = 0
            print("Closing csvfile=",self.twitterfilename)
            end_csv(self.csvfile)
            
            print("Sleep for ", self.sleeping_time, ". If you choose to stop crawling, you may CTL-C or Interrupt NOW!")
            time.sleep(self.sleeping_time)
            print("Waked up.") 

            self.twitterfilename=createfilename(dirly)
            Gtwitterfilename=self.twitterfilename
            Gcsv = start_csv(self.twitterfilename)
            self.csvwriter = Gcsv['csvwriter']
            self.csvfile = Gcsv['csvfile']
            Gcsvfile=self.csvfile
            print("new start_csv "+self.twitterfilename)
            print("counter reset.",Gtwitterfilename,"\n\n")
            print("*7* Gtwitterfilename=",Gtwitterfilename," twitterfilename=",self.twitterfilename," **")
        
    def on_error(self, status_code):
        print("on_error ",status_code)
        if status_code == 420:
            print("returning status code 420 due on_error disconnects the stream")
            print("closing csvfile ",self.twitterfilename)
            end_csv(self.csvfile)
            return False


# 24 May 2020 copies
# access token:921933333361082368-oWiQ1BErJo4ehPSugxRJFJMtgibyLTZ
# access token secret:XpKNBJGTcHeDPTQSNCqeDrSCF0KnxhBVFuIHWV2Q6QlnA
# consumer_key/API key:IRg9eRAIBRpr4pGLG0miSsm1p
# consumer_secret/API secret key: XxkhtIS7qhJiAA9i1OnG84CnzNgtw6qe3YaWCtQcek6KKgw94y

# 03 JULY 2020 copies
# Access token:  921933333361082368-F239dXeaorFHEcwnqPLyiIoF2AkiRTC
# Access token secret: tctlatGhbj1Hvxkl92CCin0KxpjhQBnOXN2Tmw0e32N6i
# consumer_key/API key: IRg9eRAIBRpr4pGLG0miSsm1p
# consumer_secret/API secret key: XxkhtIS7qhJiAA9i1OnG84CnzNgtw6qe3YaWCtQcek6KKgw94y


#NEW as of 28 JULY 2020
consumer_key = "IRg9eRAIBRpr4pGLG0miSsm1p"
consumer_secret = "XxkhtIS7qhJiAA9i1OnG84CnzNgtw6qe3YaWCtQcek6KKgw94y"
access_token = "921933333361082368-F239dXeaorFHEcwnqPLyiIoF2AkiRTC"
access_token_secret = "tctlatGhbj1Hvxkl92CCin0KxpjhQBnOXN2Tmw0e32N6i"

no_of_tweets_per_csvfile = 100
sleeping_time = 60
#dirly="C:\\Users\\User\\"
dirly=join('assets','csv')

Gtwitterfilename=createfilename(dirly)
Gcsv = start_csv(Gtwitterfilename)
Gcsvwriter = Gcsv['csvwriter']
Gcsvfile = Gcsv['csvfile']
print("*0* Gtwitterfilename=",Gtwitterfilename," **")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

myStreamListener = MyStreamListener(no_of_tweets_per_csvfile,sleeping_time,Gtwitterfilename,Gcsvwriter,Gcsvfile)
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#stream = Stream(auth, l)
#stream.filter(languages=["en"])

filen="keywords.txt"
tags = open_emotionseeds(dirly,filen)
print("tags=",tags)

while True:
    try:
        #myStream.filter(track=tags)
        myStream.filter(languages=["en"], track=tags)  ##only focus on english languages
    except Exception as e:
        print("*8* Gtwitterfilename=",Gtwitterfilename," **")
        end_csv(Gcsvfile)
        print("*9* Gtwitterfilename=",Gtwitterfilename," **")
        print('Close active file. Tweepy is shutting down')
        print('error=',e)

    #in case it faces some disconnection issue, it will go to sleep for 30 min then wake up again.
    sleep30min=30*60
    print("\n\n**sleep ",datetime.now()," for:",sleep30min,"sec in While loop")    
    time.sleep(sleep30min)

    Gtwitterfilename=createfilename(dirly)
    Gcsv = start_csv(Gtwitterfilename)
    csvwriter = Gcsv['csvwriter']
    Gcsvfile = Gcsv['csvfile']
    myStreamListener = MyStreamListener(no_of_tweets_per_csvfile,sleeping_time,Gtwitterfilename,csvwriter,Gcsvfile)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    print("waking up ",datetime.now()," after ",sleep30min,"sec**\n\n")
    print("*10* Gtwitterfilename=",Gtwitterfilename," **")

print("***end csvfile***")
end_csv(Gcsvfile)
print("***END***")