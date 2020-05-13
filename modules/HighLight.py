import pymongo
import os


def get_highlight(requests):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    data = collection.find()
    if requests.get('highlight_id') is not None:
        data = collection.find({"highlight_id": requests.get('highlight_id')})
    if requests.get('vod_id') is not None:
        data = collection.find({"vod_id": requests.get('vod_id')})
    if requests.get('channel_id') is not None:
        data = collection.find({"channel_id": requests.get('channel_id')})
    if requests.get('game') is not None:
        data = collection.find({"game": requests.get('game')})
    return data


def insert_highlight(vod_id, data):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    data = {
        'highlight_id': vod_id,
        'vod_id': vod_id,
        'channel_id': '2',
        'game': 'PUPG',
        'start_at': data['start'],
        'duration': data['duration'],
        'youtube_url': 'https://youtu.be/frguLOUro2E',
        "avg_score": 0
    }
    collection.insert(data)

    return
