import pymongo
import os
import json
import sys
import modules.Vod
from flask import Flask, request, jsonify
from flask_restful import Api
from bson.json_util import dumps
# from modules.Vod import insert_vod

app = Flask(__name__)
api = Api(app)
# sys.path.append("modules")

@app.route('/')
def home():
    return "Hello world"

@app.route('/api/vod/create', methods=["POST"])
def create():
    if request.method == 'POST' :
        data = modules.Vod.insert_vod(request.values['vod_id'])
        return jsonify(data)
@app.route('/api/vod', methods=["GET"])
def index():
    if request.method == 'GET' :
        data = modules.Vod.index()
        return dumps(data)
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
    # client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
    # db = client.ClipFetcher
    # collection = db.Vod
    # count = collection.find().count()
    count = modules.Vod.count()
    # return api.add_resource(count)
    return json.dumps(count)


if __name__ == '__main__':
    app.run()
