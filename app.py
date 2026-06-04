import os
from flask import Flask, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ROOT_DEST_URL = os.environ.get('ROOT_DEST_URL')
ALLOWED_HOST = os.environ.get('ALLOWED_HOST')


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


@app.route("/", defaults={"path": ""}, methods=HTTP_METHODS)
@app.route("/<path:path>", methods=HTTP_METHODS)
def index(path):
    if not ROOT_DEST_URL:
        return "Destination URL has to be defined!", 400
    
    if ALLOWED_HOST and ALLOWED_HOST not in (request.remote_addr, request.headers.get('Origin'), request.host):
        return "Forbidden", 403
        
    DEST_URL = f'{ROOT_DEST_URL}/{path}?{request.query_string.decode("utf-8") }'
    headers = {}
    headers.update(request.headers)
    del headers['Host']

    if request.method == 'GET':
        r = requests.get(
            DEST_URL,
            headers=headers,
            data=request.data
        )
        return r.content, r.status_code

    elif request.method == 'POST':
        data = request.data or request.form
        r = requests.post(
            DEST_URL,
            headers=headers,
            data=data
        )
        return r.content, r.status_code

    elif request.method == 'DELETE':
        r = requests.delete(
            DEST_URL,
            headers=headers
        )
        return r.content, r.status_code

    elif request.method == 'PATCH':
        data = request.data or request.form
        r = requests.patch(
            DEST_URL,
            headers=headers,
            data=data
        )
        return r.content, r.status_code

    elif request.method == 'PUT':
        data = request.data or request.form
        r = requests.put(
            DEST_URL,
            headers=headers,
            data=data
        )
        return r.content, r.status_code

    elif request.method == 'OPTIONS':
        r = requests.options(
            DEST_URL,
            headers=headers
        )
        return r.content, r.status_code

    else:
        return ''
