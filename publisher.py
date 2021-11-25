from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
import sys
import threading


space_articles = []
space_blogs = []
space_reports = []


app = Flask(__name__)

def publish_articles():
    global space_articles
    print("Scheduler is alive!")
    url = 'https://api.spaceflightnewsapi.net/v3/articles?_limit=3'
    r = requests.get(url)
    json_data = json.loads(r.text)
    # print(json_data, file=sys.stderr)
    if(len(space_articles) == 0):
        space_articles.append(json_data[0])
    for i in range(len(json_data)):
        if(json_data[i] not in space_articles):
            space_articles.append(json_data[i])

    threading.Timer(1000, publish_articles).start()



def publish_blogs():
    global space_blogs
    print("Scheduler is alive!")
    url = 'https://api.spaceflightnewsapi.net/v3/blogs?_limit=1'
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


def publish_reports():

    global space_reports
    print("Scheduler is alive!")
    url = 'https://api.spaceflightnewsapi.net/v3/reports?_limit=1'
    r = requests.get(url)
    json_data = json.loads(r.text)
    # print(json_data, file=sys.stderr)
    if(len(space_reports) == 0):
        space_reports.append(json_data[0])
    for i in range(len(json_data)):

        if(json_data[i] not in space_reports):
            space_reports.append(json_data[i])

    # print(space_articles, file=sys.stderr)
    threading.Timer(1000, publish_reports).start()

if __name__ == '__main__':
    publish_articles()
    publish_blogs()
    publish_reports()
    app.run(host='172.17.0.4', port=5005, debug=True)
