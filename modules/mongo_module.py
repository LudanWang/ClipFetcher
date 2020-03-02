import pymongo
import os

client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
db = client.ClipFetcher

def insert_vod(object):
    collection = db.Vod
    data = {
        'vod_id': object['vod_id'],
        'channel_id': object['channel_id'],
        'game': object['game'],
        'comment': object['comment']
    }
    return collection.insert(data)
