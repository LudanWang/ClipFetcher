import pymongo
import os


def insert_vod(vod_id, memo = ""):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    data = {
        'vod_id': vod_id,
        'title': 'test title',
        'channel_id': 3,
        'game': 'PUPG',
        'comment': "test",
        'youtube_url': 'https://youtu.be/frguLOUro2E',
        "avg_score": 0,
        'memo': memo
    }
    collection.insert(data)
    # test = collection.find_one({"vod_id": vod_id}, {"channel_id": 1})
    return


def index(vod_id=None):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    if vod_id:
        return collection.find_one({"vod_id": vod_id})
    else:
        return collection.find().sort("vod_id", -1)


def count():
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    return collection.find().count()


def check_vod(vod_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    return collection.find_one({"vod_id": vod_id})


def check(vod_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    return collection.find_one({"vod_id": vod_id})


def status(vod_id=None, status_code=0):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Vod
    if vod_id is not None:
        if collection.find({"vod_id": vod_id}).count() is not 0:
            status_code += 1
            if client.ClipFetcher.HighLight.find({"vod_id": vod_id}).count() is not 0:
                status_code += 1

    return status_code
