from urllib import response
from flask import Flask, Response, request
# import sqlite3
import redis
import json


# conn = sqlite3.connect("lab10.db")
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
app = Flask(__name__)

@app.route("/key", methods=['GET','POST'])
def keys():
    if request.method == 'GET':
        print(r.keys())
        return Response(json.dumps(r.keys()), status=200, mimetype='application/json')
    if request.method == 'POST':
        content = request.get_data()
        text = str(content, encoding="utf-8")
        data = json.loads(text)
        key = data['key']
        value = data['value']
        print(key, value)
        if r.get(key) == None:
            print(key,value)
            print(r.set(key,value))
            return Response("201", status=201, mimetype='application/json')
        else:
            # key exist
            return Response("400", status=400, mimetype='application/json')
    return "Hello, World"


@app.route("/key/<path:k>", methods=['GET','PUT', 'DELETE'])
def keyA(k):
    print(k)
    if request.method == 'GET':
        print(r.get(k))
        if r.get(k) == None:
            return Response(json.dumps(404), status=404, mimetype='application/json')
        else:
            response_data = {
                k: r.get(k)
            }
            return Response(json.dumps(response_data), status=200, mimetype='application/json')
    if request.method == 'PUT':
        print(r.get(k))
        content = request.get_data()
        text = str(content, encoding="utf-8")
        data = json.loads(text)
        value = data['value']
        if r.get(k) == None:
            # new key
            r.set(k, value)
            return Response("201", status=201, mimetype='application/json')
        else:
            r.set(k, value)
            return Response("200", status=200, mimetype='application/json')
    if request.method == 'DELETE':
        print(r.get(k))
        r.delete(k)
        return Response("200", status=200, mimetype='application/json')
    return "Hello, World"

@app.route("/")
def hello():
    return ""

if __name__ == '__main__':
    r.flushall()
    app.run(host='0.0.0.0')