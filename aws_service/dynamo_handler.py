import boto3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

table = dynamodb.Table("PDF_Metadata")

def save_metadata(file_id, filename):
    try:
        table.put_item(Item={
            "file_id": file_id,
            "filename": filename,
            "uploaded_at": datetime.utcnow().isoformat()
        })
    except Exception as e:
        raise RuntimeError(f"Failed to save metadata to DynamoDB: {e}")

def get_metadata(file_id):
    try:
        return table.get_item(Key={"file_id": file_id}).get("Item", {})
    except Exception as e:
        raise RuntimeError(f"Failed to get metadata: {e}")

def get_metadata(file_id):
    response = table.get_item(Key={"file_id": file_id})
    return response.get("Item", None)

def list_metadata():
    response = table.scan()
    return response.get("Items", [])
