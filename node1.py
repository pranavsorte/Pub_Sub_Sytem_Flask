from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
import sys
import threading
space_articles = []
import api_urls
app = Flask(__name__)
string = "Topic 1 notifications"


def publish_articles():
    
    global space_articles
    print("Scheduler is alive!")
    url = api_urls.api_url.get('articles')
    r = requests.get(url)
    json_data = json.loads(r.text)
    # print(json_data, file=sys.stderr)
    if(len(space_articles) == 0):
        space_articles.append(json_data[0])
    for i in range(len(json_data)):
        if(json_data[i] not in space_articles):
            space_articles.append(json_data[i])

    
    threading.Timer(1000, publish_articles).start()


@app.route('/request', methods=["GET"])
def test_2():
    global space_articles
    # print(space_articles, file=sys.stderr)
    return jsonify(space_articles)


if __name__ == '__main__':
    publish_articles()
    print(space_articles, file=sys.stderr)
    app.run(host='0.0.0.0', port=5002, debug=True)
