from flask import Flask, request
from backend.kvs_store import put,get,delete, update_store
from backend.update_metadata import update_metadata, print_metadata, check_metadata
import socket
import threading
import os
import json
app = Flask(__name__)


def handle_client(client_socket):
    data = client_socket.recv(1024)
    data = data.decode()
    data = json.loads(data)
    isUpToDate = check_metadata(data['request']['casual-metadata'])
    if isUpToDate == True:
        update_store(data['key'], data['request']['value'])
        update_metadata(data['response']['casual-metadata'])
        client_socket.close()
        print_metadata()
    else:
        print("Not to up date sorry :/")

def launch_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    this_ip = os.environ.get("SOCKET_ADDRESS")
    ip, port = this_ip.split(":")
    ADDR = (ip,8100)
    print(ADDR)
    server_socket.bind(ADDR)
    server_socket.listen(1)
    print(f"Listening for connection on {ADDR}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


@app.route('/kvs/<key>', methods=['PUT','GET','DELETE'])
def update(key):
    if request.method == 'PUT':
        data = request.get_json()
        output = put(data, key)
        print_metadata()
        if output[1] == 200 or output[1] == 201:
            ip_list = os.environ.get("VIEW").split(",")
            this_ip = os.environ.get("SOCKET_ADDRESS")
            ip_list.remove(this_ip)
            for ip in ip_list:
                ip_address, port = ip.split(":")
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((ip_address, 8100))
                payload = {
                    "key":key,
                    "request":data,
                    "response": json.loads(output[0])
                }
                payload = json.dumps(payload)
                clientSocket.send(payload.encode())


    elif request.method == 'GET':
        output = get(key)
    elif request.method == 'DELETE':
        output = delete(key)
    return output

if __name__ == "__main__":
    t = threading.Thread(target=launch_server)
    t.daemon = True
    t.start()

    this_ip = os.environ.get("SOCKET_ADDRESS")
    ip, port = this_ip.split(":")
    app.run(host=ip, port=port)
