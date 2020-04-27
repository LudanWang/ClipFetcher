import pymongo
import os


def insert(highlight_id, text, score):
    client = pymongo.MongoClient(os.environ.get('MONGODB_KEY'))
    collection = client.ClipFetcher.FeedBack
    data = {
        'highlight_id': highlight_id,
        'text': text,
        'score': score,
    }
    collection.insert(data)

    return "OK"
