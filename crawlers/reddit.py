import praw
import csv
import pandas as pd
import datetime as datetime
from datetime import datetime

reddit = praw.Reddit(client_id='2L4M15duljh4ZQ', 
                     client_secret='YeX3suRgyp-u2AFvDehx1o_twft6ww', 
                     user_agent='FYP crawler')

with open("input.txt", "r") as file:
    lines = file.readlines()
    print('lines: ', end='')
    print(lines)
    keyword = lines[0].strip('\n')
    num_post = lines[1].strip('\n')
    num_post =eval(num_post)
subreddit = reddit.subreddit(keyword)
top_subreddit = subreddit.top()
top_subreddit = subreddit.top(limit=num_post)

Cnow = datetime.now()
Cdate = Cnow.strftime("%Y-%m-%d")
Ctime = Cnow.strftime("%H:%M:%S")
Ctime2 = Cnow.strftime("%H%M%S")

for submission in subreddit.top(limit=1):
    print(submission.title, submission.id)

topics_dict = { "title":[], 
                "score":[], 
                "url_id":[], 
                "comms_num": [], 
                "created": [], 
                "body":[]}

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["url_id"].append(submission.id)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)

topics_data = pd.DataFrame(topics_dict)
topics_data

def get_date(created):
    return datetime.fromtimestamp(created)

_timestamp = topics_data["created"].apply(get_date)

topics_data = topics_data.assign(timestamp = _timestamp)
topics_data

url_id = topics_data['url_id']

for url_id in topics_data:
    url = 'https://www.reddit.com/r/malaysia/comments/'+ topics_data['url_id']
    
topics_data['url'] = url
topics_data

#csvFileDetail = '../csv/RD_details_'+keyword+'_'+Cdate+'_'+Ctime+'.csv'
topics_data.to_csv('../csv/RD_details_'+keyword+'_'+Cdate+'_'+Ctime2+'.csv', index=False) 

url_list = topics_data['url']
print(url_list)



csvFileComment = '../csv/RD_comment_'+keyword+'_'+Cdate+'_'+Ctime2+'.csv'
with open(csvFileComment, 'w', newline='',encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["author", "comment", "URL", "Comment Time", "Crawl Time"])
    
for url in url_list:
    submission = reddit.submission(url=url)
    
    with open(csvFileComment, 'a+', newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
            
        for top_level_comment in submission.comments:
            
            
            try:
                comtime = top_level_comment.created_utc
                author = top_level_comment.author
            
                def get_date_time(comtime):
                    return datetime.fromtimestamp(comtime)
            
                comment_time = get_date_time(comtime)
                print(top_level_comment.body)
                writer.writerow([author, top_level_comment.body, url, comment_time, (Cdate + Ctime)])
            except:
                print("error "+str(IOError))
                continue