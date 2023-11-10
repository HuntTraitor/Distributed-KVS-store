from flask import Flask, request
from backend.kvs_store import put,get,delete
from backend.communication import communication_thread, broadcast, real_broadcast
import threading
import os
app = Flask(__name__)

@app.route('/kvs/<key>', methods=['PUT','GET','DELETE'])
def update(key):
    # write an if output == 503, sleep 1 seconds and retry request shrug
    if request.method == 'PUT':
        data = request.get_json()
        output = put(data, key)
        real_broadcast(key, data, request.method)
    elif request.method == 'GET':
        data = request.get_json()
        output = get(data, key)
        real_broadcast(key, data, request.method)
    elif request.method == 'DELETE':
        data = request.get_json()
        output = delete(data, key)
        real_broadcast(key, data, request.method)
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
    t = threading.Thread(target=communication_thread)
    t.daemon = True
    t.start()

    this_ip = os.environ.get("SOCKET_ADDRESS")
    ip, port = this_ip.split(":")
    app.run(host=ip, port=port)
