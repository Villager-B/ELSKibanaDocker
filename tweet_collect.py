import json, config
from requests_oauthlib import OAuth1Session
from pprint import pprint
import time
from datetime import datetime, timedelta, timezone
import pandas as pd
import time

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

col = [
    "tweet_id",
    "text",
    'user_name',
    'user_id',
    "urls",
    "favorite_count",
    "retweet_count",
    "tweet_url",
    "created_at"]

df = pd.DataFrame(columns=col)
url = "https://api.twitter.com/1.1/favorites/list.json"
params = {"screen_name":"nitkcdadon",
          "count":200,
          'include_entities':'true'}
res = twitter.get(url, params = params)
count = 0
all_count = 0
max_id = str()

if res.status_code == 200:
    timelines = json.loads(res.text)

for tl in timelines:
    all_count += 1
    
    tweet_id = tl["id_str"]
    text = tl["text"]
    try:
        urls = tl["entities"]["urls"]
        if len(urls) == 0:
            urls = "null"
        if urls == "[]":
            urls = "null"
    except:
        urls = "null"
    user_name = tl['user']['name']
    user_id = tl['user']['id_str']
    favorite_count = tl["favorite_count"]
    retweet_count = tl["retweet_count"]
    created_at = tl["created_at"]
    tweet_url = 'https://twitter.com/' + tl['user']['screen_name'] + '/status/' + tl['id_str']
    
    
    count += 1
    df_line = pd.DataFrame([[tweet_id,text,user_name,user_id,urls,favorite_count,retweet_count,tweet_url,created_at]],
                       columns=col)
    df = df.append(df_line, ignore_index=True)
    max_id = tweet_id

flag = 0

while flag == 0:
    time.sleep(5)
    url = "https://api.twitter.com/1.1/favorites/list.json"
    params = {"screen_name":"nitkcdadon",
              "count":200,
              'include_entities':'false'}
    if res.status_code == 200:
        timelines = json.loads(res.text)

    for tl in timelines:
        all_count += 1

        tweet_id = tl["id_str"]
    
        if  len(df[df['tweet_id'] == tweet_id]) == 1:
            flag = 1
            continue
        
    
        text = tl["text"]

        try:
            urls = str(tl["entities"]["urls"])
            if len(urls) == 0:
                urls = "null"
            if urls == "[]":
                urls = "null"
        except:
            urls = "null"
        user_name = tl['user']['name']
        user_id = tl['user']['id_str']
        favorite_count = tl["favorite_count"]
        retweet_count = tl["retweet_count"]
        tweet_url = 'https://twitter.com/' + tl['user']['screen_name'] + '/status/' + tl['id_str']
        created_at = tl["created_at"]
        count += 1
        df_line = pd.DataFrame([[tweet_id,text,user_name,user_id,urls,favorite_count,retweet_count,tweet_url,created_at]],
                       columns=col)
        df = df.append(df_line, ignore_index=True)
        max_id = tweet_id


JST = timezone(timedelta(hours=+9), 'JST')
now = datetime.now(JST)

if now.month < 10:
    month = '0'+ str(now.month)
else:
    month = now.month
    
if now.day < 10:
    day = '0'+ str(now.day)
else:
    day = now.day
    
date = str(now.year) + '-' + str(month) + '-' + str(day)

df.to_csv('fav_tweets_' + date + '.csv',index=False)