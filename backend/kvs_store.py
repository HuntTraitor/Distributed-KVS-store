import json
import time
from .update_metadata import create_metadata, check_metadata, update_metadata

#initializing store
store = {}
num_retries = 2

def put(data, key):
    if 'value' not in data or 'causal-metadata' not in data:
        return json.dumps({"error": "PUT request does not specify a value"}), 400

    isUpToDate = check_metadata(data['causal-metadata'])
    if isUpToDate == True:
        if len(key) > 50:
            return json.dumps({"error":"Key is too long"}), 400
        elif key in store:
                store[key] = data['value']
                if 'broadcasted-metadata' in data:
                    update_metadata(data['broadcasted-metadata'])
                    causal_metadata = data['broadcasted-metadata']
                else:
                    causal_metadata = create_metadata()
                    update_metadata(causal_metadata)
                return json.dumps({"result":"replaced", "causal-metadata": f"{causal_metadata}"}), 200
        else:
            store[key] = data['value']
            if 'broadcasted-metadata' in data:
                update_metadata(data['broadcasted-metadata'])
                causal_metadata = data['broadcasted-metadata']
            else:
                causal_metadata = create_metadata()
                update_metadata(causal_metadata)
            return json.dumps({"result":"created", "causal-metadata": f"{causal_metadata}"}), 201
    else:
        retries = num_retries
        while retries > 0:
            time.sleep(1)
            isUpToDate = check_metadata(data['causal-metadata'])
            if isUpToDate:
                return put(data, key)
            retries -= 1
        return json.dumps({"error": "causal dependencies not satisfied; try again later"}), 503

def get(data, key):
    isUpToDate = check_metadata(data['causal-metadata'])
    if isUpToDate == True:
        if key in store:
            if 'broadcasted-metadata' in data:
                update_metadata(data['broadcasted-metadata'])
                causal_metadata = data['broadcasted-metadata']
            else:
                causal_metadata = create_metadata()
                update_metadata(causal_metadata)
            return json.dumps({"result": "found", "value": store[key], "causal-metadata": f"{causal_metadata}"}), 200
        else: 
            return json.dumps({"error": "Key does not exist"}), 404
    else:
        retries = num_retries
        while retries > 0:
            time.sleep(1)
            isUpToDate = check_metadata(data['causal-metadata'])
            if isUpToDate:
                return get(data, key)
            retries -= 1
        return json.dumps({"error":"causal dependencies not satisfied; try again later"}), 503

def delete(data, key):
    isUpToDate = check_metadata(data['causal-metadata'])
    if isUpToDate == True:
        if key in store:
            store.pop(key)
            if 'broadcasted-metadata' in data:
                update_metadata(data['broadcasted-metadata'])
                causal_metadata = data['broadcasted-metadata']
            else:
                causal_metadata = create_metadata()
                update_metadata(causal_metadata)
            return json.dumps({"result":"deleted", "causal-metadata": f"{causal_metadata}"}), 200
        else:
            return json.dumps({"error":"Key does not exist"}), 404
    else:
        retries = num_retries
        while retries > 0:
            time.sleep(1)
            isUpToDate = check_metadata(data['causal-metadata'])
            if isUpToDate:
                return delete(data, key)
            retries -= 1
        return json.dumps({"error":"causal dependencies not satisfied; try again later"}), 503

# helpers

def print_store():
    print(store)

def get_store():
    return store

def update_store(updated_store):
    global store
    store = updated_store