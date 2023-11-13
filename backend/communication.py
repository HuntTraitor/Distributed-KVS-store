import os
import requests
import json

def broadcast(key, data, request, output): # kvs
    if output[1] == 200 or output[1] == 201:
        output = json.loads(output[0])
        data['broadcasted-metadata'] = output['causal-metadata']
        ip_list = os.environ.get("VIEW").split(",")
        this_ip = os.environ.get("SOCKET_ADDRESS")
        ip_list.remove(this_ip)
        for ip in ip_list:
            url = f"http://{ip}/kvs/broadcast/{key}"
            try:
                if request == 'PUT':
                    response = requests.put(url, json=data, timeout=2)
                elif request == 'GET':
                    response = requests.get(url, json=data, timeout=2)
                elif request == 'DELETE':
                    response = requests.delete(url, json=data, timeout=2)
            except requests.exceptions.RequestException:
                # kvs request failed -> ip is down
                #   so delete ip from every existing replica's view
                for jp in ip_list+[this_ip]:
                    if jp != ip:
                        url = f"http://{jp}/view/broadcast"
                        addr = {"socket-address":f"{ip}"}
                        response = requests.delete(url, json=addr)
                        
def view_broadcast(data, request, output): # view
    if output[1] == 200 or output[1] == 201:
        output = json.loads(output[0])
        ip_list = os.environ.get("VIEW").split(",")
        this_ip = os.environ.get("SOCKET_ADDRESS")
        ip_list.remove(this_ip)
        for ip in ip_list:
            url = f"http://{ip}/view/broadcast"
            try:
                if request == 'PUT':
                    response = requests.put(url, json=data, timeout=2)
                elif request == 'GET':
                    response = requests.get(url, json=data, timeout=2)
                elif request == 'DELETE':
                    response = requests.delete(url, json=data, timeout=2)
            except:
                # request failed -> ip is down
                #   so delete ip from every existing replica's view
                for jp in ip_list+[this_ip]:
                    if jp != ip:
                        url = f"http://{jp}/view/broadcast"
                        response = requests.delete(url, json=data)      
