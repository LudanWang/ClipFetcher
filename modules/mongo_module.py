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
    collection.insert(data)
    test = collection.find_one({"vod_id": object['vod_id']}, {"channel_id": 1})
    return test['channel_id']

def index(data):
    collection = db.Vod
    return collection.find()