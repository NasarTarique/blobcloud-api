from azure.storage.blob import BlobServiceClient  , BlobClient , __version__
import os


local_path = "./data"
os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
os.environ['STORAGE_CONTAINER'] = 'test-container'
local_file_name = 'test.txt'
upload_file_path = os.path.join(local_path,local_file_name)

# Create a container for Azurite for the first run
print('azure storage version '+__version__+' python quickstart sample')
blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),)
try:
    blob_client =blob_service_client.get_blob_client(container=os.environ['STORAGE_CONTAINER'],blob=local_file_name)
    print("\n Uploading to azure storage as blob :\n\t"+local_file_name)
    with open(upload_file_path,"rb") as data:
        blob_client.upload_blob(data)


except Exception as e:
   print(e)