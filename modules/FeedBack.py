import pymongo
import os
import modules.HighLight


def insert(highlight_id, text, score):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.FeedBack
    data = {
        'highlight_id': highlight_id,
        'text': text,
        'score': score,
    }
    collection.insert(data)
    update_avg_score(highlight_id, score)
    return "OK"

def update_avg_score(highlight_id, score):
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    collection = client.ClipFetcher.FeedBack

    avg_score = 0.0
    count = 0
    for x in collection.find({},{ "_id": 0, "score": 1}):
        avg_score += int(x['score'])
        count += 1
    avg_score = avg_score / count

    modules.HighLight.update_avg_score(highlight_id, round(avg_score, 1))

    return
    
