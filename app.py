from flask import Flask, request, jsonify
from backend.kvs_store import put,get,delete
from backend.update_system import broadcast
from backend.update_metadata import update_metadata, create_metadata
import socket
import threading
import os
import time
app = Flask(__name__)


def handle_client(client_socket):
    print(f"Got your message!")
    client_socket.close()

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

        ip_list = os.environ.get("VIEW").split(",")
        this_ip = os.environ.get("SOCKET_ADDRESS")
        ip_list.remove(this_ip)
        print(f"THIS IP: {this_ip}")
        for ip in ip_list:
            ip_address, port = ip.split(":")
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((ip_address, 8100))


    elif request.method == 'GET':
        output = get(key)
    elif request.method == 'DELETE':
        output = delete(key)
    return output

if __name__ == "__main__":
    t = threading.Thread(target=launch_server)
    t.start()

    time.sleep(1)

    this_ip = os.environ.get("SOCKET_ADDRESS")
    ip, port = this_ip.split(":")
    app.run(host=ip, port=port)
