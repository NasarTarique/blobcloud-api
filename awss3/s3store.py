import boto3
import logging
import os
from botocore.exceptions import ClientError


os.environ['AWS_ACCESS_KEY_ID'] = "AKIAIOSFODNN7EXAMPLE"
os.environ['AWS_SECRET_ACCESS_KEY'] ="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" 
client = boto3.client(
    's3',
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
    endpoint_url='http://127.0.0.1:9444/s3/'
)

    #endpoint_url='http://172.17.0.1:9444/s3/'
client.create_bucket(Bucket="rivendell")
