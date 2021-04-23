import time
import csv
from datetime import datetime
from apiclient.discovery import build
import pandas as pd
from os.path import join

#Comment CSV
Gyoutubefilename=" "
Gcsvfile=" "

def start_csv(csvfilename):
    global Gyoutubefilename
    global Gcsvfile
    csvfile=open(csvfilename, 'w', newline='', encoding="utf-8")    
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['comment_id',
                        'video_id',
                        'video_url',
                        'comment_url',
                        'text_original',
                        'author_name',
                        'author_img_url',
                        'author_channel_url',
                        'can_rate',
                        'viewer_rating',
                        'like_count',
                        'published_at',
                        'updated_at',
                        'crawled_date',
                        'crawled_time',
                        'can_reply',
                        'total_reply_count',
                        'is_public',
                       ])
    
    Gyoutubefilename=csvfilename
    print("*1* Gyoutubefilename=",Gyoutubefilename," youtubefilename=",csvfilename," **")
    return {'csvwriter':csvwriter, 'csvfile':csvfile}


def createfilename(dirly):
    global Gyoutubefilename
    anow = datetime.now()
    adatetime = anow.strftime("%m%d%Y_%H%M%S")
    Gyoutubefilename = dirly+"youtube_"+keyword+"_"+adatetime+".csv"    
    print(Gyoutubefilename, " newly created.")
    print("*4* Gyoutubefilename=",Gyoutubefilename," **")
    return Gyoutubefilename

def end_csv(csvfile):
    print("Closing "+Gyoutubefilename)
    print("*3* Gyoutubefilename=",Gyoutubefilename," **")
    csvfile.close()
    return

def append_data(comment_id,
                video_id, 
                video_url,
                comment_url,
                text_original,
                author_name,
                author_img_url,
                author_channel_url,
                can_rate,
                viewer_rating,
                like_count,
                published_at,
                updated_at,
                crawled_date,
                crawled_time,
                can_reply,
                total_reply_count,
                is_public):
    global Gyoutubefilename
    global Gcsvfile
    with open(Gyoutubefilename, 'a+') as csvfile:
        fieldnames = ['comment_id',
                        'video_id',
                        'video_url',
                        'comment_url',
                        'text_original',
                        'author_name',
                        'author_img_url',
                        'author_channel_url',
                        'can_rate',
                        'viewer_rating',
                        'like_count',
                        'published_at',
                        'updated_at',
                        'crawled_date',
                        'crawled_time',
                        'can_reply',
                        'total_reply_count',
                        'is_public']
        writer = csv.DictWriter(Gcsvfile, fieldnames =fieldnames)
        writer.writerow({
                        'comment_id':comment_id,
                        'video_id':video_id, 
                        'video_url':video_url,
                        'comment_url':comment_url,
                        'text_original':text_original,
                        'author_name':author_name,
                        'author_img_url':author_img_url,
                        'author_channel_url':author_channel_url,
                        'can_rate':can_rate,
                        'viewer_rating':viewer_rating,
                        'like_count':like_count,
                        'published_at':published_at,
                        'updated_at':updated_at,
                        'crawled_date':crawled_date,
                        'crawled_time':crawled_time,
                        'can_reply':can_reply,
                        'total_reply_count':total_reply_count,
                        'is_public':is_public
                        })
        
#Create 2nd CSV for replies
Gyoutubefilename1=" "
Gcsvfile1=" "

def start_csv1(csvfilename):
    global Gyoutubefilename1
    global Gcsvfile1
    csvfile=open(csvfilename, 'w', newline='', encoding="utf-8")    
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['replies_id',
                     'replies_video_id', 
                     'replies_video_url',
                     'replies_url',
                     'replies_text_original',
                     'replies_parent_id',
                     'author_name',
                     'author_img_url',
                     'author_channel_url',
                     'can_rate',
                     'viewer_rating',
                     'like_count',
                     'published_at',
                     'updated_at',
                     'crawled_date',
                     'crawled_time'
                       ])
    
    Gyoutubefilename1=csvfilename1
    print("*1* Gyoutubefilename1=",Gyoutubefilename1," youtubefilename1=",csvfilename1," **")
    return {'csvwriter':csvwriter, 'csvfile':csvfile}


def createfilename1(dirly):
    global Gyoutubefilename1
    anow = datetime.now()
    adatetime = anow.strftime("%m%d%Y_%H%M%S")
    Gyoutubefilename1 = dirly+"youtube_"+"reply_"+keyword+"_"+adatetime+".csv"    
    print(Gyoutubefilename1, " newly created.")
    print("*4* Gyoutubefilename1=",Gyoutubefilename1," **")
    return Gyoutubefilename1

def end_csv1(csvfile):
    print("Closing "+Gyoutubefilename1)
    print("*3* Gyoutubefilename1=",Gyoutubefilename1," **")
    csvfile.close()
    return

def append_data1(replies_id,
                 replies_video_id, 
                 replies_video_url,
                 replies_url,
                 replies_text_original,
                 replies_parent_id,
                 author_name,
                 author_img_url,
                 author_channel_url,
                 can_rate,
                 viewer_rating,
                 like_count,
                 published_at,
                 updated_at,
                 crawled_date,
                 crawled_time):
    global Gyoutubefilename1
    global Gcsvfile1
    with open(Gyoutubefilename1, 'a+') as csvfile:
        fieldnames = ['replies_id',
                     'replies_video_id', 
                     'replies_video_url',
                     'replies_url',
                     'replies_text_original',
                     'replies_parent_id',
                     'author_name',
                     'author_img_url',
                     'author_channel_url',
                     'can_rate',
                     'viewer_rating',
                     'like_count',
                     'published_at',
                     'updated_at',
                     'crawled_date',
                     'crawled_time']
        writer = csv.DictWriter(Gcsvfile1, fieldnames =fieldnames)
        writer.writerow({
                     'replies_id':replies_id,
                     'replies_video_id':replies_video_id, 
                     'replies_video_url':replies_video_url,
                     'replies_url':replies_url,
                     'replies_text_original':replies_text_original,
                     'replies_parent_id':replies_parent_id,
                     'author_name':author_name,
                     'author_img_url':author_img_url,
                     'author_channel_url':author_channel_url,
                     'can_rate':can_rate,
                     'viewer_rating':viewer_rating,
                     'like_count':like_count,
                     'published_at':published_at,
                     'updated_at':updated_at,
                     'crawled_date':crawled_date,
                     'crawled_time':crawled_time
                        })

#Func to get comments + replies
def get_all_comments(video_id):
    #comments = []
    next_page_token = None
    yt_url= 'https://www.youtube.com/watch?v='
    
    while 1:
        Cnow = datetime.now()
        Cdate = Cnow.strftime("%Y-%m-%d")
        Ctime = Cnow.strftime("%H:%M:%S")
        
        request= youtube.commentThreads().list(part='snippet, replies',
                                                videoId= video_id,
                                                maxResults=100,
                                                #order="relevance",
                                                pageToken=next_page_token).execute()
        #comments += request['items']
        
        for item in request["items"]:
            total_reply_count = 0
            replies = None
            comment = item["snippet"]["topLevelComment"]
            comment_id = item["id"]
            video_id = comment["snippet"]["videoId"]
            video_url = yt_url + video_id
            comment_url = video_url + "&lc=" + comment_id
            text_original = comment["snippet"]["textDisplay"]
            author_name = comment["snippet"]["authorDisplayName"]
            author_img_url = comment["snippet"]["authorProfileImageUrl"]
            author_channel_url = comment["snippet"]["authorChannelUrl"]
            can_rate = comment["snippet"]["canRate"]
            viewer_rating = comment["snippet"]["viewerRating"]
            like_count = comment["snippet"]["likeCount"]
            published_at = comment["snippet"]["publishedAt"]
            updated_at = comment["snippet"]["updatedAt"]
            crawled_date = Cdate
            crawled_time = Ctime
            can_reply = item["snippet"]["canReply"]
            total_reply_count = item["snippet"]["totalReplyCount"]
            is_public = item["snippet"]["isPublic"]

            append_data(comment_id,
                         video_id, 
                         video_url,
                         comment_url,
                         text_original,
                         author_name,
                         author_img_url,
                         author_channel_url,
                         can_rate,
                         viewer_rating,
                         like_count,
                         published_at,
                         updated_at,
                         crawled_date,
                         crawled_time,
                         can_reply,
                         total_reply_count,
                         is_public)
            
            #Write replies
            try: 
                if total_reply_count > 0:
                    for replies in item["replies"]["comments"]:
                        replies_id = replies["id"]
                        replies_video_id = replies["snippet"]["videoId"]
                        replies_video_url = video_url  
                        replies_url = video_url + "&lc=" + replies_id
                        replies_text_original = replies["snippet"]["textDisplay"]
                        replies_parent_id = replies["snippet"]["parentId"]
                        author_name = replies["snippet"]["authorDisplayName"]
                        author_img_url = replies["snippet"]["authorProfileImageUrl"]
                        author_channel_url = replies["snippet"]["authorChannelUrl"]
                        can_rate = replies["snippet"]["canRate"]
                        viewer_rating = replies["snippet"]["viewerRating"]
                        like_count = replies["snippet"]["likeCount"]
                        published_at = replies["snippet"]["publishedAt"]
                        updated_at = replies["snippet"]["updatedAt"]
                        crawled_date = Cdate
                        crawled_time = Ctime
                        
                        append_data1(replies_id,
                                     replies_video_id, 
                                     replies_video_url,
                                     replies_url,
                                     replies_text_original,
                                     replies_parent_id,
                                     author_name,
                                     author_img_url,
                                     author_channel_url,
                                     can_rate,
                                     viewer_rating,
                                     like_count,
                                     published_at,
                                     updated_at,
                                     crawled_date,
                                     crawled_time)
                        
            except Exception as e:
                print(e)
                continue

        
        next_page_token = request.get('nextPageToken')
        
        if next_page_token is None:
            break
            
            
    #return comments

#Insert how many videos that would like to crawl
#num_video = 3

with open("input.txt", "r") as file:
    lines = file.readlines()
    print('lines: ', end='')
    print(lines)
    keyword = lines[0].strip('\n')
    num_video = lines[1].strip('\n')
    num_video =eval(num_video)
#Marvel Entertainment

dirly=join('assets','csv')
#Create comment csv
Gyoutubefilename=createfilename(dirly)
Gcsv = start_csv(Gyoutubefilename)
Gcsvwriter = Gcsv['csvwriter']
Gcsvfile = Gcsv['csvfile']
print("*0* Gyoutubefilename=",Gyoutubefilename," **")

#Create Replies csv
Gyoutubefilename1=createfilename1(dirly)
Gcsv1 = start_csv(Gyoutubefilename1)
Gcsvwriter1 = Gcsv1['csvwriter']
Gcsvfile1 = Gcsv1['csvfile']
print("*0* Gyoutubefilename1=",Gyoutubefilename1," **")


#Seach based on keyword & get video_id
api_key = 'AIzaSyDeVZrKoqc5Les5gbikLIO13xInQi6o7vA'
youtube = build('youtube','v3',developerKey=api_key)
#Marvel Entertainment
res = youtube.search().list(q= keyword , 
                            part='snippet',
                            type='video', 
                            #publishedAfter=start_time,
                            #publishedBefore=end_time,
                            maxResults= num_video).execute()

#Need to get the videoID 
video_id = []

for item in res['items']:
    print(item['id']['videoId'])
    print(item['snippet']['title'])
    #video_id += (item['id']['videoId'])
    video_id.append(item['id']['videoId'])

print(video_id)


#Get All comments & replies
#comments = []
for x in range(num_video):
    get_all_comments(video_id[x])
    x += 1

#Close both csv
end_csv(Gcsvfile)
end_csv1(Gcsvfile1)

print('END ALREADY')