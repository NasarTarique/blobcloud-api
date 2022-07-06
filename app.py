from flask import Flask , request , make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from azblob.azureclient import AzureClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///example.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from models import  *

def custom_error(message, status_code): 
    return make_response(jsonify(message), status_code)

@app.route("/",methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    token = request.headers.get('Authorization')
    user = UserKeys.query.filter_by(api_key=token).first()
    az = AzureClient()
    try:
        blob = az.read(filename,auth=True if user else False)
    except Exception as e:
        return  custom_error("File not Found ", 404)
    
    return blob

@app.route("/",methods=['POST'])
def post_file():
    token = request.headers.get('Authorization')
    user = UserKeys.query.filter_by(api_key=token).first()
    if user:
        azure = AzureClient()
        if 'file' not in request.files:
            return "No files uploaded"
        file = request.files['file']
        filename = file.filename
        azure.upload(file,filename)
        return f"file {filename} uploaded"
    else:
        return custom_error("Forbidden", 403)


@app.route('/generatekey/',methods=['POST'])
def generate_key():
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    try:
        us = UserKeys(name,email,pwd)
    except:
        return  custom_error("Failed to generate API key",400)
    db.session.add(us)
    db.session.commit()
    api_key = us.api_key
    return api_key


# test blobs
@app.route("/list",methods=['GET'])
def list_blobs():
    token = request.headers.get('Authorization')
    az = AzureClient()
    blobs = az.listfiles()
    return '\n'.join([blob.name for blob in blobs])