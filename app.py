from flask import Flask, request
from backend.kvs_store import put,get,delete, get_store
from backend.communication import broadcast
from backend.update_metadata import get_metadata
from backend.view_store import put as put_view, get as get_view, delete as delete_view
from backend.startup import startup
import os
import json

app = Flask(__name__)

@app.route('/kvs/<key>', methods=['PUT','GET','DELETE'])
def update(key):
    if request.method == 'PUT':
        data = request.get_json()
        output = put(data, key)
        broadcast(key, data, request.method, output)
    elif request.method == 'GET':
        data = request.get_json()
        output = get(data, key)
        broadcast(key, data, request.method, output)
    elif request.method == 'DELETE':
        data = request.get_json()
        output = delete(data, key)
        broadcast(key, data, request.method, output)
    return output

@app.route('/kvs/broadcast/<key>', methods=['PUT','GET','DELETE'])
def update_repliace(key):
    if request.method == 'PUT':
        data = request.get_json()
        output = put(data, key)
    elif request.method == 'GET':
        data = request.get_json()
        output = get(data, key)
    elif request.method == 'DELETE':
        data = request.get_json()
        output = delete(data, key)
    return output


@app.route('/view', methods=['PUT','GET','DELETE'])
def manage_view():
    if request.method == 'PUT':
        data = request.get_json()
        output = put_view(data.get('socket-address'))
    elif request.method == 'GET':
        output = get_view()
    elif request.method == 'DELETE':
        data = request.get_json()
        output = delete_view(data.get('socket-address'))
    return output

@app.route('/update', methods=['GET'])
def return_store():
    store_data = get_store()
    metadata = get_metadata()
    return json.dumps({"data": store_data, "metadata": metadata}), 200

with app.app_context():
    startup()

if __name__ == "__main__":
    this_ip = os.environ.get("SOCKET_ADDRESS")
    ip, port = this_ip.split(":")
    app.run(host=ip, port=port)