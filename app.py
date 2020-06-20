import pymongo
import os
import json
import sys
import modules.FeedBack, modules.Vod, modules.HighLight, modules.Opinion
from flask import Flask, request, jsonify, abort, Response
from flask_restful import Api
from bson.json_util import dumps
from ChatCrawler import getVodInformation
from BaseAlgorithm import frequencyAlgo
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
api = Api(app)
CORS(app)


def run_analysis(vod_id, new_highlight_id, memo):
    print("status: 0")
    getVodInformation(vod_id)
    print("status: 1")
    data = frequencyAlgo(vod_id)
    print("status: 2")
    modules.HighLight.insert_highlight(vod_id, new_highlight_id, memo, data)
    print("status: 3")


# sys.path.append("modules")

# /api/vod/appraise
@app.route('/')
def home():
    return "Hello world"


# Vod
@app.route('/api/vod', methods=['GET', 'POST'])
def vod():
    if request.method == 'POST':
        requests = request.json
        vod_id = requests['vod_id']
        memo = requests['memo']
        if not vod_id:
            abort(501, description="不能為空")
        
        modules.Vod.insert_vod(vod_id, memo)
        # if modules.Vod.check_vod(vod_id) is not None:
        # abort(400, description="vod_id 已分析過")
        new_highlight_id = modules.HighLight.get_new_highlight(vod_id)
        modules.HighLight.insert_first_highlight(new_highlight_id, vod_id, memo)
        Thread(target=run_analysis, args=(vod_id, new_highlight_id, memo)).start()

        data = {
            'highlight_id': new_highlight_id,
        }
        return Response(dumps(data), mimetype='application/json')
    if request.method == 'GET':
        vod_id = request.values.get('vod_id')
        if vod_id:
            data = modules.Vod.index(vod_id)
        else:
            data = modules.Vod.index()

        return Response(dumps(data), mimetype='application/json')

@app.route('/api/vod/check', methods=['POST'])
def check():
    if request.method == 'POST':
        requests = request.json
        vod_id = requests['vod_id']
        data = modules.Vod.check(vod_id)
        if data:
            return '', 204
        else:
            return abort(403)


# status_code:
# 0:還未有 vod 資料
# 1:分析進行中
# 2:分析完成
@app.route('/api/vod/status', methods=['POST'])
def status():
    if request.method == 'POST':
        data = request.json
        if data['vod_id'] is None:
            return abort(400, description="vod_id 無資料")
        status_code = modules.Vod.status(data['vod_id'])
        return jsonify({"status": status_code})


# Highlight
@app.route('/api/vod/highlight', methods=['GET'])
def vod_highlight():
    if request.method == 'GET':
        requests = request.values
        data = modules.HighLight.get_highlight(requests)
        if data:
            return Response(dumps(data), mimetype='application/json')
        else:
            return abort(400, description="搜尋不存在")


# Feedback
@app.route('/api/vod/appraise', methods=['POST'])
def appraise():
    if request.method == 'POST':
        data = request.json
        modules.FeedBack.insert(data['highlight_id'], data['text'], data['score'])
        return '', 204


# Opinion
@app.route('/api/opinion', methods=['GET', 'POST'])
def opinion():
    if request.method == 'POST':
        requests = request.json
        modules.Opinion.insert(requests)
        return '', 204
    if request.method == 'GET':
        data = modules.Opinion.index()
        return Response(dumps(data), mimetype='application/json')

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
    # collection = db.Vod
    db.Vod.remove({})
    db.HighLight.remove({})
    db.Opinion.remove({})
    db.FeedBack.remove({})

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
