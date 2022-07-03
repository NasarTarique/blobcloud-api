from azure.storage.blob import BlobServiceClient ,ContainerClient 
import os

os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
os.environ['STORAGE_CONTAINER'] = 'test-container'
CONNECTION_STRING =  os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER")

class AzureClient:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    
    def check_auth(self):
        pass

    def azupload(self,fileblob,filename):
        blob_client = self.blob_service_client.get_blob_client(CONTAINER_NAME,blob=filename)
        blob_client.upload_blob(fileblob)

    def azread(self,filename):
        blob_client = self.blob_service_client.get_blob_client(CONTAINER_NAME,blob=filename)
        blob =blob_client.download_blob()
        url  = blob_client.url
        return url
    
    def azdelete(self,filename):
        blob_client = self.blob_service_client.get_blob_client(CONTAINER_NAME,blob=filename)
        blob_client.delete_blob()

    def azlist(self):
        container = ContainerClient.from_connection_string(conn_str=CONNECTION_STRING, container_name=CONTAINER_NAME)
        blob_list = container.list_blobs()
        return blob_list