from flask import jsonify
import os
import json
from .update_metadata import create_metadata, check_metadata

#initializing store
store = {}

def put(data, key): # Hunter
    if 'value' not in data or 'casual-metadata' not in data:
        return jsonify({"error": "PUT request does not specify a value"}), 400
    
    isUpToDate = check_metadata(data['casual-metadata'])
    if isUpToDate == True:
        if len(key) > 50:
            return jsonify({"error":"Key is too long"}), 400
        elif key in store:
                store[key] = data['value']
                casual_metadata = create_metadata()
                return json.dumps({"result":"replaced", "casual-metadata": f"{casual_metadata}"}), 200 # we need to broadcast casual_metadata here to the other instances to put them in their memory
        else:
            store[key] = data['value']
            casual_metadata = create_metadata()
            return json.dumps({"result":"created", "casual-metadata": f"{casual_metadata}"}), 201
    elif isUpToDate == False:
        return "Not up to date sorry"



def get(key): # Alan
    if key in store: 
        return jsonify({"result": "found", "value": store[key]}), 200
    else: 
        return jsonify({"error": "Key does not exist"}), 404

def delete(key): # David
    if key in store:
        store.pop(key)
        return jsonify({"result":"deleted"}), 200
    else:
        return jsonify({"error":"Key does not exist"}), 404

def update_store(key, value):
    store[key] = value