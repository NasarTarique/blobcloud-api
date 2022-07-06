from azure.storage.blob import BlobServiceClient ,ContainerClient , generate_blob_sas, AccessPolicy , ContainerSasPermissions
import os
from datetime import datetime , timedelta

os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
os.environ['STORAGE_CONTAINER'] = 'test-container'
os.environ['ACCOUNT_NAME']  = 'devstoreaccount1'
os.environ['ACCOUNT_KEY']  = 'Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
CONNECTION_STRING =  os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER")
ACCOUNT_NAME = os.environ.get('ACCOUNT_NAME')
ACCOUNT_KEY = os.environ.get('ACCOUNT_KEY')

class AzureClient:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))
        self.identifiers = {}
        self.get_access_policy_identifiers()

    def get_access_policy_identifiers(self):
        container_client = self.blob_service_client.get_container_client(CONTAINER_NAME)
        container_policies = container_client.get_container_access_policy()
        if 'auth_users' and 'guest_users' in container_policies.keys():
            self.identifiers['auth_users'] = container_policies['auth_users']
            self.identifiers['guest_users'] = container_policies['guest_users']
        else:
            access_policy = AccessPolicy(permission=ContainerSasPermissions(read=True),
                                         expiry=datetime.utcnow()+timedelta(hours=1),
                                         start=datetime.utcnow()-timedelta(minutes=1))
            self.identifiers['guest_users'] = access_policy
            access_policy = AccessPolicy(permission=ContainerSasPermissions(read=True,write=True,delete=True),
                                         expiry=datetime.utcnow()+timedelta(days=364),
                                         start=datetime.utcnow())
            self.identifiers['auth_users'] = access_policy
            container_client.set_container_access_policy(signed_identifiers=self.identifiers)

    def generate_sas_authusers(self,filename):
        sas_token = generate_blob_sas(ACCOUNT_NAME,CONTAINER_NAME,filename,account_key=ACCOUNT_KEY,policy_id='auth_users')
        return sas_token
    
    def generate_sas_guestusers(self,filename):
        sas_token = generate_blob_sas(ACCOUNT_NAME,CONTAINER_NAME,filename,account_key=ACCOUNT_KEY,policy_id='guest_users')
        return sas_token


    def create_connection_string(self,accountname,accountkey):
        pass
    
    def createcontainer(self,container):
        container_client = ContainerClient(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),container_name=container)
        container_client.create_container()

    def upload(self,fileblob,filename):
        blob_client = self.blob_service_client.get_blob_client(CONTAINER_NAME,blob=filename)
        blob_client.upload_blob(fileblob)

    def read(self,filename,auth=False):
        blob_client = self.blob_service_client.get_blob_client(CONTAINER_NAME,blob=filename)
        url  = blob_client.url
        sas_token=''
        if auth:
            sas_token = self.generate_sas_authusers(filename)
        else:
            sas_token = self.generate_sas_guestusers(filename)

        return {
            'url':url,
            'sas':sas_token
        }
    
    def delete(self,filename):
        blob_client = self.blob_service_client.get_blob_client(CONTAINER_NAME,blob=filename)
        blob_client.delete_blob()

    def listfiles(self):
        container = ContainerClient.from_connection_string(conn_str=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"), container_name=CONTAINER_NAME)
        blob_list = container.list_blobs()
        return blob_list