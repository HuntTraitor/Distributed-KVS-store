from flask import jsonify
import json

# initializing store for view
view_store = []

def put(addr): # assumes addr is in the form: <IP:PORT> as dealt with in app.py
    if addr in view_store:
        return jsonify({"result": "already present"}), 200
    else:
        view_store.append(addr)
        return jsonify({"result": "added"}), 201

def get(addr):
    return jsonify({"view": view_store}), 200

def delete(addr):
    if addr in view_store:
        view_store.remove(addr)
        return jsonify({"result": "deleted"}), 200
    else:
        return jsonify({"error": "View has no such replica"}), 404
