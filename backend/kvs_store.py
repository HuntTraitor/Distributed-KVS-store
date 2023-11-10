from flask import jsonify
import json
from .update_metadata import create_metadata, check_metadata, update_metadata

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
                update_metadata(casual_metadata)
                return json.dumps({"result":"replaced", "casual-metadata": f"{casual_metadata}"}), 200
        else:
            store[key] = data['value']
            casual_metadata = create_metadata()
            update_metadata(casual_metadata)
            return json.dumps({"result":"created", "casual-metadata": f"{casual_metadata}"}), 201
    else:
        return jsonify({"error": "Casual dependencies not satisfied; try again later"}), 503


def get(data, key):
    isUpToDate = check_metadata(data['casual-metadata'])
    if isUpToDate == True:
        if key in store: 
            casual_metadata = create_metadata()
            update_metadata(casual_metadata)
            return json.dumps({"result": "found", "value": store[key], "casual-metadata": f"{casual_metadata}"}), 200
        else: 
            return json.dumps({"error": "Key does not exist"}), 404
    else:
        return jsonify({"error":"Casual dependencies not satisfied; try again later"}), 503


def delete(data, key): # David
    isUpToDate = check_metadata(data['casual-metadata'])
    if isUpToDate == True:
        if key in store:
            store.pop(key)
            casual_metadata = create_metadata()
            update_metadata(casual_metadata)
            return json.dumps({"result":"deleted", "casual-metadata": f"{casual_metadata}"}), 200
        else:
            return json.dumps({"error":"Key does not exist"}), 404
    else:
        # we need to resend the data if this occurs
        return jsonify({"error":"Casual dependencies not satisfied; try again later"}), 503

def update_store(key, request, value=None):
    if request == 'PUT':
        store[key] = value
    elif request == 'DELETE':
        store.pop(key)

def print_store():
    print(store)