import pymongo
import os


def insert_vod(vod_id):
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    collection = client.ClipFetcher.Vod
    data = {
        'vod_id': vod_id,
        'channel_id': 1,
        'game': 'PUPG',
        'comment': "test"
    }
    collection.insert(data)
    # test = collection.find_one({"vod_id": vod_id}, {"channel_id": 1})
    return 'OK'


def index():
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    collection = client.ClipFetcher.Vod
    return collection.find()


def count():
    client = pymongo.MongoClient(os.environ('MONGODB_KEY'))
    collection = client.ClipFetcher.Vod
    return collection.find().count()


def check(vod_id):
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    collection = client.ClipFetcher.Vod
    return collection.find_one({"vod_id": vod_id})


def status(vod_id, highlight_id):
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    collection = client.ClipFetcher.Vod
    return 'OK'
