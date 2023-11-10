import json
from .update_metadata import create_metadata, check_metadata, update_metadata

#initializing store
store = {}

def put(data, key):
    if 'value' not in data or 'casual-metadata' not in data:
        return json.dumps({"error": "PUT request does not specify a value"}), 400

    isUpToDate = check_metadata(data['casual-metadata'])
    if isUpToDate == True:
        if len(key) > 50:
            return json.dumps({"error":"Key is too long"}), 400
        elif key in store:
                store[key] = data['value']
                if 'broadcasted-metadata' in data:
                    update_metadata(data['broadcasted-metadata'])
                    casual_metadata = data['broadcasted-metadata']
                else:
                    casual_metadata = create_metadata()
                    update_metadata(casual_metadata)
                return json.dumps({"result":"replaced", "casual-metadata": f"{casual_metadata}"}), 200
        else:
            store[key] = data['value']
            if 'broadcasted-metadata' in data:
                update_metadata(data['broadcasted-metadata'])
                casual_metadata = data['broadcasted-metadata']
            else:
                casual_metadata = create_metadata()
                update_metadata(casual_metadata)
            return json.dumps({"result":"created", "casual-metadata": f"{casual_metadata}"}), 201
    else:
        return json.dumps({"error": "Casual dependencies not satisfied; try again later"}), 503

def get(data, key):
    isUpToDate = check_metadata(data['casual-metadata'])
    if isUpToDate == True:
        if key in store:
            if 'broadcasted-metadata' in data:
                update_metadata(data['broadcasted-metadata'])
                casual_metadata = data['broadcasted-metadata']
            else:
                casual_metadata = create_metadata()
                update_metadata(casual_metadata)
            return json.dumps({"result": "found", "value": store[key], "casual-metadata": f"{casual_metadata}"}), 200
        else: 
            return json.dumps({"error": "Key does not exist"}), 404
    else:
        return json.dumps({"error":"Casual dependencies not satisfied; try again later"}), 503

def delete(data, key):
    isUpToDate = check_metadata(data['casual-metadata'])
    if isUpToDate == True:
        if key in store:
            store.pop(key)
            if 'broadcasted-metadata' in data:
                update_metadata(data['broadcasted-metadata'])
                casual_metadata = data['broadcasted-metadata']
            else:
                casual_metadata = create_metadata()
                update_metadata(casual_metadata)
            return json.dumps({"result":"deleted", "casual-metadata": f"{casual_metadata}"}), 200
        else:
            return json.dumps({"error":"Key does not exist"}), 404
    else:
        return json.dumps({"error":"Casual dependencies not satisfied; try again later"}), 503


def print_store():
    print(store)