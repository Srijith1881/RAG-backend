# aws_service/query_log_handler.py

import boto3
import os
from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()
dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
'''dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)'''

table = dynamodb.Table("QueryLog")


def log_query(run_id, query_text, response_text, confidence_score, file_id="unknown"):
    try:
        item = {
            "run_id": run_id,
            "query_text": query_text,
            "response_text": response_text,
            "confidence_score": Decimal(str(confidence_score)),
            "file_id": file_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)
        print("✅ Logged query to QueryLog")

    except Exception as e:
        print(f"❌ Failed to log query: {e}")
