import pymongo
import os


def getHighlight(highlight_id):
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    collection = client.ClipFetcher.HighLight
    data = collection.find({"highlight_id": highlight_id})

    return data
