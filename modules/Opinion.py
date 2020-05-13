import pymongo
import os


def insert(requests):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Opinion
    data = {
        'mail': requests['mail'],
        'content': requests['content'],
    }
    collection.insert(data)

    return "OK"


def index():
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.Opinion
    return collection.find().sort('_id', -1)
