# -*- coding:utf-8 -*-

import requests, json, os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Set the bearer token
bearer_token = os.environ.get("APIKEY")

# Set the headers with the bearer token
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

app = Flask(__name__)
# app.debug = True

columns = ['Name', 'Image', 'Update At', 'Purchase At', 'code', '']

def getAllData():
    returnData = []
    page = 1
    
    while True:
        data = requests.get("https://api.envato.com/v3/market/buyer/list-purchases", params={'page': page}, headers=headers).json()
        for i in range(len(data['results'])):
            returnData.append([
                f"<a href=\"{data['results'][i]['item']['url']}\" target=\"_blank\">{data['results'][i]['item']['name']}</a>",
                f"<img src=\"{data['results'][i]['item']['previews']['landscape_preview']['landscape_url'] if data['results'][i]['item']['previews'].get('landscape_preview') else ''}\"></img>",
                datetime.fromisoformat(data['results'][i]['item']['updated_at']).strftime('%Y-%m-%d'),
                datetime.fromisoformat(data['results'][i]['sold_at']).strftime('%Y-%m-%d'),
                data['results'][i]['code'],
                '<button type="button" class="btn btn-success" onclick="download(this)">Download</button>',
            ])
        if data['count'] < data['pagination']['page_size'] * page:
            break
        else:
            page = page + 1

    return returnData

@app.route('/')
def index():
    return render_template('index.html', columns=columns)

@app.route('/_server_data')
def get_server_data():   
    return json.dumps({'aaData': getAllData()})

@app.route('/get_download_link', methods=['POST'])
def get_download_link():
    requestData = request.get_json()
    data = requests.get("https://api.envato.com/v3/market/buyer/download", params={'purchase_code': requestData['code']}, headers=headers).json()
    return data['download_url']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
