import os
import uuid
from functools import wraps
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///addons.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Resource(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    location = db.Column(db.String(255), nullable=True)

with app.app_context():
    db.create_all()

HEROKU_ADDON_ID = os.environ.get('HEROKU_ADDON_ID', 'default-addon-id')
HEROKU_ADDON_PASSWORD = os.environ.get('HEROKU_ADDON_PASSWORD', 'default-addon-password')

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != HEROKU_ADDON_ID or auth.password != HEROKU_ADDON_PASSWORD:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/heroku/resources', methods=['POST'])
@requires_auth
def provision():
    # Read the --location option passed via the Heroku CLI
    payload = request.get_json() or {}
    options = payload.get('options', {})
    location = options.get('location', os.environ.get('LOCATION', 'https://www.example.com'))

    resource = Resource(location=location)
    db.session.add(resource)
    db.session.commit()
    return jsonify({
        'id': resource.id,
        'config': { 'REQUESTS_PROXY_URL': f"{request.host_url}proxy/{resource.id}" },
        'message': 'Successfully provisioned proxy add-on.'
    }), 200

@app.route('/heroku/resources/<id>', methods=['DELETE'])
@requires_auth
def deprovision(id):
    resource = Resource.query.get(id)
    if resource:
        db.session.delete(resource)
        db.session.commit()
    return '', 204

@app.route('/heroku/resources/<id>', methods=['PUT'])
@requires_auth
def update_plan(id):
    payload = request.get_json() or {}
    options = payload.get('options', {})
    location = options.get('location')

    resource = Resource.query.get(id)
    if not resource:
        return jsonify({'error': 'Not found'}), 404
        
    if location:
        resource.location = location
        db.session.commit()
        
    return '', 200


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route("/proxy/<resource_id>/", defaults={"path": ""}, methods=HTTP_METHODS)
@app.route("/proxy/<resource_id>/<path:path>", methods=HTTP_METHODS)
def index(resource_id, path):
    resource = Resource.query.get(resource_id)
    if not resource:
        return "Resource not found", 404
        
    dest_url_base = resource.location
    if not dest_url_base:
        return "Destination URL has to be defined (LOCATION)!", 400
    
    DEST_URL = f'{dest_url_base}/{path}?{request.query_string.decode("utf-8") }'
    headers = {}
    headers.update(request.headers)
    headers.pop('Host', None)

    data = request.data or request.form
    r = requests.request(
        method=request.method,
        url=DEST_URL,
        headers=headers,
        data=data
    )
    return r.content, r.status_code
