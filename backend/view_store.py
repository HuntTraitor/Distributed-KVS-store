from flask import jsonify
import os

# get VIEW as a list
view = os.environ.get("VIEW").split(",")

def put(addr): # assumes addr is in the form: <IP:PORT> as dealt with in app.py
    if addr in view:
        return jsonify({"result": "already present"}), 200
    else:
        view.append(addr)
        os.environ["VIEW"] = ",".join(view)
        return jsonify({"result": "added"}), 201

def get():
    return jsonify({"view": view}), 200

def delete(addr):
    if addr in view:
        view.remove(addr)
        os.environ["VIEW"] = ",".join(view)
        return jsonify({"result": "deleted"}), 200
    else:
        return jsonify({"error": "View has no such replica"}), 404

