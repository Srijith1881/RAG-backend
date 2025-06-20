
# Handles S3 interactions

import boto3
import botocore
import os
from dotenv import load_dotenv

load_dotenv()

# AWS Production Configuration (COMMENTED)
# s3 = boto3.client(
#     "s3",
#     region_name=os.getenv("REGION", "ap-south-1"),
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
# )

# LocalStack Configuration
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name=os.getenv("REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
)

bucket = os.getenv("BUCKET_NAME")

def upload_to_s3(file_path, key):
    # Uploads a local file to the configured S3 bucket
    try:
        s3.upload_file(file_path, bucket, key)
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Failed to upload to S3: {e}")

def download_from_s3(key, dest_path):
    # Downloads a file from S3 to the specified destination path.
    try:
        s3.download_file(bucket, key, dest_path)
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Failed to download from S3: {e}")