from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
import sys
import threading
space_reports = []
import api_urls

app = Flask(__name__)
string = "Topic 3 notifications"


def publish_reports():
    
    global space_reports
    print("Scheduler is alive!")
    url = api_urls.api_url.get('reports')
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


@app.route('/request', methods=["GET"])
def test_2():
    global space_reports
    # print(space_articles, file=sys.stderr)
    return jsonify(space_reports)


if __name__ == '__main__':
    publish_reports()
    app.run(host='0.0.0.0', port=5004, debug=True)
