import pymongo
import os

def insert_vod(vod_id):
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    db = client.ClipFetcher.Vod
    collection = db
    data = {
        'vod_id': vod_id,
        'channel_id': 1,
        'game': 'PUPG',
        'comment': "test"
    }
    collection.insert(data)
    test = collection.find_one({"vod_id": vod_id}, {"channel_id": 1})
    return test['channel_id']

def index():
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    db = client.ClipFetcher.Vod
    collection = db
    return collection.find()

def count():
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    db = client.ClipFetcher.Vod
    collection = db
    return collection.find().count()