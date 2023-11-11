from flask import Flask, request
from backend.kvs_store import put,get,delete
from backend.communication import broadcast
from backend.update_metadata import print_metadata
import os
app = Flask(__name__)

@app.route('/kvs/<key>', methods=['PUT','GET','DELETE'])
def update(key):
    if request.method == 'PUT':
        data = request.get_json()
        output = put(data, key)
        broadcast(key, data, request.method, output) # might need to run this in another thread
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
    
if __name__ == "__main__":
    this_ip = os.environ.get("SOCKET_ADDRESS")
    ip, port = this_ip.split(":")
    app.run(host=ip, port=port)