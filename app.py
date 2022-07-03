from flask import Flask , request
from azblob.azureclient import AzureClient

app = Flask(__name__)

@app.route("/",methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    az = AzureClient()
    blob = az.azread(filename)
    return blob
    

@app.route("/",methods=['POST'])
def post_file():
    filename = request.data['filename']
    blob = request.data['filename']

# test blobs
@app.route("/list",methods=['GET'])
def list_blobs():
    az = AzureClient()
    blobs = az.azlist()
    return ''.join([blob.name for blob in blobs])
    




