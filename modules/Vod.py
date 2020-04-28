import pymongo
import os


def insert_vod(vod_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    data = {
        'vod_id': vod_id,
        'channel_id': 1,
        'game': 'PUPG',
        'comment': "test",
        'youtube_url': 'https://youtu.be/frguLOUro2E',
        "avg_score": 0
    }
    collection.insert(data)
    # test = collection.find_one({"vod_id": vod_id}, {"channel_id": 1})
    return


def index(vod_id=None):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    if vod_id is None:
        return collection.find()
    else:
        return collection.find({"vod_id": vod_id})


def count():
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    return collection.find().count()


def check(vod_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    return collection.find_one({"vod_id": vod_id})


def status(vod_id, highlight_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    return 'OK'
