import boto3
import logging
import os
from botocore.exceptions import ClientError


os.environ['AWS_ACCESS_KEY_ID'] = "AKIAIOSFODNN7EXAMPLE"
os.environ['AWS_SECRET_ACCESS_KEY'] ="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" 
os.environ['BUCKET_NAME'] = 'rivendell'

class S3Client:
    def __init__(self):
        self.s3client = boto3.client(
            's3',
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
            endpoint_url='http://127.0.0.1:9444/s3/'
        )
    

    def presigned_url_authusers(self,filename):
        response = self.s3client.generate_presigned_url('get_object',Params={
            'Bucket':os.environ.get("BUCKET_NAME"),
            'Key':filename
        },
        ExpiresIn=604800
        )
        return response

    def presigned_url_guestusers(self,filename):
        response = self.s3client.generate_presigned_url('get_object',Params={
            'Bucket':os.environ.get("BUCKET_NAME"),
            'Key':filename
        },
        ExpiresIn=300
        )
        return response

    def createbucket(self,bucket):
        self.s3client.create_bucket(Bucket=bucket)
    
    def upload(self,fileblob,filename):
        response = self.s3client.upload_fileobj(fileblob,os.environ.get("BUCKET_NAME"),filename)

    def read(self,filename,auth=False):
        if auth:
            url  = self.presigned_url_authusers(filename)
            return {
                'url':url[0:url.index('?')],
                'presigned_url':url
            }
        else:
            return {
                'presigned_url':self.presigned_url_guestusers(filename)
            }
    
    def delete(self,filename):
        self.s3client.delete_object(Bucket=os.environ.get("BUCKET_NAME"),Key='filname')
    
    def listfiles(self):
        pass

aws = S3Client()
aws.delete('test.txt')
print(aws.read('something.txt'))
with open('./data/something.txt', 'rb') as f:
    aws.upload(f,'something.txt')
print(aws.read('something.txt'))
print(aws.read('something.txt',auth=True))
aws.delete('something.txt')