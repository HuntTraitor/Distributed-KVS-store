import os
import socket
import threading
from .kvs_store import check_metadata, update_store
from .update_metadata import update_metadata
import json

def broadcast(key, output, data, request):
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
                "request-type":request,
                "request":data,
                "response": json.loads(output[0])
            }
            payload = json.dumps(payload)
            clientSocket.send(payload.encode())


def handle_client(client_socket):
    data = client_socket.recv(1024)
    data = data.decode()
    data = json.loads(data)
    isUpToDate = check_metadata(data['request']['casual-metadata'])
    if isUpToDate == True:
        if data['request-type'] == 'PUT':
            update_store(data['key'], data['request-type'], data['request']['value'])
            update_metadata(data['response']['casual-metadata'])
            client_socket.close()
        elif data['request-type'] == 'GET':
            update_metadata(data['response']['casual-metadata'])
            client_socket.close()
        elif data['request-type'] == 'DELETE':
            update_store(data['key'], data['request-type'])
            update_metadata(data['response']['casual-metadata'])
            client_socket.close()
    else:
        # sleep one second and retry the request shrug
        print("Not to up date sorry :/")


def communication_thread():
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
        # print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()