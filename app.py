import pymongo
import os
import json
import sys
from flask import Flask, request
from flask_restful import Api
from pprint import pprint

app = Flask(__name__)
api = Api(app)
sys.path.append("modules")

@app.route('/')
def home():
    return "Hello world"

@app.route('/api/vod/create', methods=["GET"])
def create():
    if request.method == 'GET' :
        import vod_module
        vod_module.create(request.values['vod_id'])
        return 'OK'
@app.route('/insert')
def mongo():
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    db = client.ClipFetcher
    collection = db.Vod
    test = {
        'id': '20170101',
        'name': 'test',
        'age': 20,
        'gender': 'male'
    }
    collection.insert(test)

    return "OK"


@app.route("/db")
def mongo2():
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    db = client.ClipFetcher
    collection = db.Vod
    result = collection.find({'name': 'Jordan'})
    print(result)
    # print(os.environ['MONGODB'])

    return "OK"


@app.route("/delete")
def mongo3():
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    db = client.ClipFetcher
    collection = db.Vod
    result = collection.remove({'name': '*'})
    print(result)

    return 'OK'


@app.route("/count")
def count():
    client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    db = client.ClipFetcher
    collection = db.Vod
    count = collection.find().count()

    # return api.add_resource(count)
    return json.dumps(count)


if __name__ == '__main__':
    app.run()
