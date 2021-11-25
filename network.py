from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
import sys
import threading
space_articles = []

app = Flask(__name__)

@app.route('/')
def test():
    return 'Hi'

@app.route('/connect', methods=["POST","GET"])
def connect():
    topic = request.get_data()
    print(topic, file=sys.stderr)
    # content = {}
    if topic == b'Space Articles':
        url_1 = 'http://172.17.0.2:5002/request'
        content = requests.get(url_1)
        content_data = json.loads(content.text)
        # print(jsonify(content),file=sys.stderr)
        return jsonify(content_data)
    elif topic == b'Space Blogs':
        url_2 = 'http://172.17.0.3:5003/request'
        content = requests.get(url_2)
        content_data = json.loads(content.text)
        # print(jsonify(content),file=sys.stderr)
        return jsonify(content_data)
    elif topic == b'Space Reports':
        url_3 = 'http://172.17.0.4:5004/request'
        content = requests.get(url_3)
        content_data = json.loads(content.text)
        # print(jsonify(content),file=sys.stderr)
        return jsonify(content_data)
    else:
        return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
