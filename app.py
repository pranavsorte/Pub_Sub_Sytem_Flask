import json
from flask.helpers import flash
import requests
from flask import Flask, render_template, request, redirect
import requests, json
from flask.json import jsonify
import pymongo
from pymongo import MongoClient
import sys
from datetime import datetime
import threading

custom_id = 0
app = Flask(__name__)


def get_db():
    client = MongoClient(host="test_mongodb", port=27017, authSource='admin')
    db = client["users_db"]
    return db

def stringify(content_topic):
    data = []
    for i in range(len(content_topic)):
        row_data = []
        row_data.append(content_topic[i]["title"])
        row_data.append(content_topic[i]["url"])
        row_data.append(content_topic[i]["summary"])
        row_data.append(content_topic[i]["publishedAt"])

        data.append(row_data)
    
    return data


@app.route('/', methods=["POST","GET"])
def ping_server():
    db = get_db()
    if(request.method == "POST"):
        name = request.form["name"]
        email = request.form["email"]
        option = request.form["topics"]
        # print(option)
        if(option == "Space_blogs"):
            topic_initial = 'Space Blogs'
        if(option == "Space_articles"):
            topic_initial = 'Space Articles'
        if(option == "Space_reports"):
            topic_initial = 'Space Reports'
        single_data = {
            "name":name,
            "email":email,
            "topic":topic_initial
        }
        db.users_tb.insert_one(single_data)
        # flash('You have subscribed to the topic!', 'info')
    

    # db_topic_a = get_db_topic_A()
    

    return render_template('index.html')

@app.route('/notifications', methods=["GET","POST"])
def notify():
    db = get_db()
    if(request.method == "POST"):
        email = request.form["email"]
        topics_list = db.users_tb.find({"email":email}, {"_id":0,"name":0,"email":0})
        # records= []
        published_data = []
        topics = []
        for record in topics_list:
            # records.append(record)
            topic = record.get('topic')
            topics.append(topic)

        for topic in topics:
            url = 'http://172.17.0.6:5001/connect'
            content_topic = requests.post(url, data=topic)
            print(content_topic.text, file=sys.stderr)
            content_list = json.loads(content_topic.text)
                # print(type(content_list),file=sys.stderr)
            data = stringify(content_list)
            published_data.append(data)
            #     print(data, file = sys.stderr)
        
    # #     threading.Timer(10, notify)
        return render_template('notifications.html', data=published_data)
    # # threading.Timer(10, notify)
    return render_template('notifications.html')



@app.route('/unsubscribe', methods=["POST", "GET"])
def unsubscribe():
    db = get_db()
    # print("topic")
    if(request.method == "POST"):
        email = request.form["email"]
        option = request.form["topics"]
        if(option == "Space_blogs"):
            topic = 'Space Blogs'
        if(option == "Space_articles"):
            topic = 'Space Articles'
        if(option == "Space_reports"):
            topic = 'Space Reports'
        # data = db.users_tb.find({'email':email,'topic':topic})
        # print("topic")
        # print(topic)
        # if(data):
        db.users_tb.remove({'email':email, 'topic':topic})
        return render_template('unsubscribe.html')

    return render_template('unsubscribe.html')


@app.route('/searchsubscriptions', methods=["POST", "GET"])
def search():
    db = get_db()
    if(request.method == "POST"):
        email = request.form["email"]
        # topic = request.form["topics"]
        data = db.users_tb.find({'email': email})
        print(data)
        if(data):
            return render_template('seachsubscriptions.html', data=data)

    return render_template('seachsubscriptions.html')



@app.route('/subscriptions')
def fetch_users():
    db = get_db()
    _users = db.users_tb.find()
    users = [{"name": user["name"], "email": user["email"], "topic": user["topic"]} for user in _users]
    return jsonify(users)

if __name__ == '__main__':

    app.run(host = '0.0.0.0', debug=True, threaded=True)
