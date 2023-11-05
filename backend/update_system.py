import os
from flask import request
import requests


def broadcast(key, request, data=None):
    ip_list = os.environ.get("VIEW").split(",")
    this_ip = os.environ.get("SOCKET_ADDRESS")
    ip_list.remove(this_ip)
    for ip in ip_list:
        url = f"http://{ip}/listen/{key}"
        requests.put(url, json=data)