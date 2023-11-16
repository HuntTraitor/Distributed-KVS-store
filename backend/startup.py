import os
import requests
from .update_metadata import update_metadata_list
from .kvs_store import update_store
def startup():
    this_ip = os.environ.get("SOCKET_ADDRESS")
    views = os.environ.get("VIEW").split(",")
    for view in views:
        try:
            url = f"http://{view}/view"
            addr = {"socket-address":f"{this_ip}"}
            response = requests.put(url, json=addr, timeout=1)
            # if this succeeds
            store_url = f"http://{view}/update"
            store_response = requests.get(store_url)
            update_store(store_response.json()['data'])
            update_metadata_list(store_response.json()['metadata'])
            
        except:
            # print(f"failed: {url}")
            pass
