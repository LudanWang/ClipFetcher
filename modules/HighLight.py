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


def insert_first_highlight(highlight_id, vod_id, memo):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    data = {
        'highlight_id': highlight_id,
        'vod_id': vod_id,
        'channel_id': '',
        'streamerName': '',
        'game': '',
        'start_at': '',
        'duration': '',
        'youtube_url': '',
        "avg_score": '',
        'memo': memo,
    }
    collection.insert(data)

    return

def insert_highlight(vod_id, highlight_id, memo, data):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    collection.update_one({'highlight_id': highlight_id}, {'$set':{
        'vod_id': vod_id,
        'channel_id': str(data['channel_id']),
        'streamerName': data['streamerName'],
        'game': data['game'],
        'start_at': data['start'],
        'duration': data['duration'],
        'youtube_url': '',
        "avg_score": 0
        }
    })

    return

def update_highlight_youtube(highlight_id, youtube_url):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.HighLight
    collection.update_one({'highlight_id': highlight_id}, {'$set':{
            'youtube_url': youtube_url
        }
    })
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
        return 'ClipFetcher_' + vod_id + '001'
    else:
        is_define = collection.find_one({'vod_id': vod_id}, sort=[('highlight_id', -1)])
        new_highlight = int(is_define['highlight_id'])
        new_highlight += 1
        return 'ClipFetcher_' + str(new_highlight)