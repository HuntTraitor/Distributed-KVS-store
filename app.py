from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "index"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)