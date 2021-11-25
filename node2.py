from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
import sys
import threading

from requests import api
space_blogs = []
import api_urls

app = Flask(__name__)
string = "Topic 2 notifications"


def publish_blogs():
    global space_blogs
    print("Scheduler is alive!")
    url = api_urls.api_url.get('blogs')
    r = requests.get(url)
    json_data = json.loads(r.text)
    # print(json_data, file=sys.stderr)
    if(len(space_blogs) == 0):
        space_blogs.append(json_data[0])
    for i in range(len(json_data)):

        if(json_data[i] not in space_blogs):
            space_blogs.append(json_data[i])

    # print(space_articles, file=sys.stderr)
    threading.Timer(1000, publish_blogs).start()


@app.route('/request', methods=["GET"])
def test_2():
    global space_blogs
    # print(space_articles, file=sys.stderr)
    return jsonify(space_blogs)


if __name__ == '__main__':
    publish_blogs()
    app.run(host='0.0.0.0', port=5003, debug=True)
