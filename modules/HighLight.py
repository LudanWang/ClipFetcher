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


def insert_first_highlight(highlight_id, vod_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    data = {
        'highlight_id': highlight_id,
        'vod_id': vod_id,
        'channel_id': None,
        'streamerName': None,
        'game': None,
        'start_at': None,
        'duration': None,
        'youtube_url': None,
        "avg_score": None,
        'memo': None,
    }
    collection.insert(data)

    return

def insert_highlight(vod_id, highlight_id, memo, data):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    collection.update_one({'highlight_id': highlight_id}, {'$set':{
        'vod_id': vod_id,
        'channel_id': data['channel_id'],
        'streamerName': data['streamerName'],
        'game': data['game'],
        'start_at': data['start'],
        'duration': data['duration'],
        'youtube_url': 'https://youtu.be/frguLOUro2E',
        "avg_score": 0,
        'memo': memo
        }
    })

    return

def update_avg_score(highlight_id, score):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    collection.update_one({'highlight_id': highlight_id}, {'$set':{'avg_score': score}})

    return

def is_define(highlight_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    is_define = collection.find({'highlight_id': highlight_id})
    if list(is_define) == []:
        return False
    else:
        return True

def get_new_highlight(vod_id):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    is_define = collection.find_one({'vod_id': vod_id})
    
    if is_define is None:
        return vod_id + '001'
    else:
        is_define = collection.find_one({'vod_id': vod_id}, sort=[('highlight_id', -1)])
        new_highlight = int(is_define['highlight_id'])
        new_highlight += 1
        return str(new_highlight)