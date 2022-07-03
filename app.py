from flask import Flask , request
from azblob.azureclient import AzureClient

app = Flask(__name__)

@app.route("/",methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    az = AzureClient()
    blob = az.read(filename)
    return blob

@app.route("/",methods=['POST'])
def post_file():
    azure = AzureClient()
    if 'file' not in request.files:
        return "No files uploaded"
    file = request.files['file']
    filename = file.filename
    azure.upload(file,filename)
    return f"file {filename} uploaded"

# test blobs
@app.route("/list",methods=['GET'])
def list_blobs():
    az = AzureClient()
    blobs = az.listfiles()
    return ''.join([blob.name+'\n' for blob in blobs])