import boto3
import botocore
import os
from dotenv import load_dotenv
load_dotenv()


s3 = boto3.client(
    "s3",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
bucket = "srbucket1881"

'''s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

bucket = "pdf-storage"'''

def upload_to_s3(file_path, key):
    try:
        s3.upload_file(file_path, bucket, key)
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Failed to upload to S3: {e}")

def download_from_s3(key, dest_path):
    try:
        s3.download_file(bucket, key, dest_path)
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Failed to download from S3: {e}")
