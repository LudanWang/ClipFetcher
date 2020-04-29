import pymongo
import os


def get_highlight(highlight_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    data = collection.find_one({"highlight_id": highlight_id})

    return data


def insert_highlight(vod_id, data):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    data = {
        'highlight_id': vod_id,
        'vod_id': vod_id,
        'channel_id': 1,
        'game': 'PUPG',
        'start_at': data['start'],
        'duration': data['duration'],
        'youtube_url': 'https://youtu.be/frguLOUro2E',
        "avg_score": 0
    }
    collection.insert(data)

    return
