import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime, timedelta, timezone

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

df = pd.read_csv('fav_tweets_' + date + '.csv')
df.fillna("don't exist",inplace=True)

mapping = {
    "mappings" : {
            "properties" : {
                "tweet": {"type":"text"},
                "user_name": {"type":"text"},
                "user_id": {"type":"long"},
                "urls": {"type":"text"},
                "favorite_count": {"type":"long"},
                "retweet_count": {"type":"long"},
                "tweet_url": {"type":"text"},
                "created_at": {"type":"date",
                              'format':'EEE LLL dd HH:mm:ss Z yyyy'},
        }
    }
}
client = Elasticsearch("http://localhost:9200")

# client.indices.delete('like_tweets')
client.indices.create(index='like_tweets', body=mapping)

def es_doc_generator(index,df):
    records =  [d[1] for d in df.iterrows()]
    docs_es = [{key: doc[key] for key in doc.keys()} for doc in records]
    for doc in docs_es:
        tid = doc['tweet_id']
        yield {
            "_index": index,
            "_id": tid,
            "_type": "_doc",
            "_source": doc,
        }
        
helpers.bulk(client,es_doc_generator("like_tweets",df))
client.close()