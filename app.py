import pymongo
import os
import json
import sys
import modules.Vod
import modules.HighLight
import modules.FeedBack
from flask import Flask, request, jsonify, abort, Response
from flask_restful import Api
from bson.json_util import dumps
from ChatCrawler import getVodInformation
from BaseAlgorithm import frequencyAlgo
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# sys.path.append("modules")

# /api/vod/appraise
# /api/vod/opinion
@app.route('/')
def home():
    return "Hello world"

# Vod
@app.route('/api/vod', methods=['GET', 'POST'])
def vod():
    if request.method == 'POST':
        vod_id = request.form.get('vod_id')
        modules.Vod.insert_vod(vod_id)

        getVodInformation(vod_id)

        # data = frequencyAlgo(vod_id)
        # modules.HighLight.insert_highlight(vod_id, data)

        return '', 204
    if request.method == 'GET':
        if request.values.get('vod_id') is None:
            data = modules.Vod.index()
        else:
            data = modules.Vod.index(request.values.get('vod_id'))

        return Response(dumps(data), mimetype='application/json')


@app.route('/api/vod/check', methods=['POST'])
def check():
    if request.method == 'POST':
        data = modules.Vod.check(request.form.get('vod_id'))
        if data is None:
            return abort(403)
        else:
            return '', 204

# TODO 進度分析未完成
@app.route('/api/vod/status', methods=['POST'])
def status():
    if request.method == 'POST':
        data = modules.Vod.status(request.form.get('vod_id'), request.form.get('highlight_id'))
        return '', 204


# Highlight
@app.route('/api/vod/highlight', methods=['GET'])
def vodHighlight():
    if request.method == 'GET':
        data = modules.HighLight.getHighlight(request.values['highlight_id'])
        return Response(dumps(data), mimetype='application/json')


# Feedback
@app.route('/api/vod/appraise', methods=['POST'])
def insert():
    if request.method == 'POST':
        print(request.form.get('highlight_id'))
        data = modules.FeedBack.insert(request.form.get('highlight_id'), request.form.get('text'), request.form.get('score'))
        return '', 204


# @app.route('/insert')
# def mongo():
#     client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
#     db = client.ClipFetcher
#     collection = db.Vod
#     test = {
#         'id': '20170101',
#         'name': 'test',
#         'age': 20,
#         'gender': 'male'
#     }
#     collection.insert(test)
#
#     return "OK"
#
#
# @app.route("/db")
# def mongo2():
#     client = pymongo.MongoClient(os.environ['MONGODB_KEY'])
#     db = client.ClipFetcher
#     collection = db.Vod
#     result = collection.find({'name': 'Jordan'})
#     print(result)
#     # print(os.environ['MONGODB'])
#
#     return "OK"
#
#
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
    # client = pymongo.MongoClient('mongodb+srv://ludan:r57035708@clipfetcher-7c9my.mongodb.net/test?retryWrites=true&w=majority')
    # db = client.ClipFetcher
    # collection = db.Vod
    # count = collection.find().count()
    count = modules.Vod.count()
    if count > 0:
        # return '', 204
        abort(403, description="數量大於 1")
    # return api.add_resource(count)
    return json.dumps(count)


if __name__ == '__main__':
    app.run()
