import boto3
from datetime import datetime
import os
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

# AWS Production Configuration (COMMENTED)
# dynamodb = boto3.resource(
#     "dynamodb",
#     region_name=os.getenv("REGION", "ap-south-1"),
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
# )

# LocalStack Configuration
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name=os.getenv("REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
)

def convert_float_to_decimal(obj):
    """Convert float values to Decimal for DynamoDB compatibility"""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_float_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_float_to_decimal(item) for item in obj]
    else:
        return obj

def log_query(run_id, query_text, response_text, confidence_score, file_id="unknown"):
    try:
        table = dynamodb.Table("QueryLog")
        
        # Convert confidence_score to Decimal
        confidence_decimal = Decimal(str(confidence_score)) if isinstance(confidence_score, (float, int)) else confidence_score
        
        item = {
            "run_id": str(run_id),  # Ensure string
            "query_text": str(query_text),  # Ensure string
            "response_text": str(response_text),  # Ensure string
            "confidence_score": confidence_decimal,  # Convert to Decimal
            "file_id": str(file_id),  # Ensure string
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Double-check all float values are converted
        item = convert_float_to_decimal(item)
        
        table.put_item(Item=item)
        print(f"✅ Query logged successfully for run_id: {run_id}")
        
    except Exception as e:
        print(f"❌ Failed to log query: {e}")
        print(f"Debug info - run_id: {run_id}, confidence_score: {confidence_score} (type: {type(confidence_score)})")
        
        # Try to log with minimal data to diagnose the issue
        try:
            table = dynamodb.Table("QueryLog")
            minimal_item = {
                "run_id": str(run_id),
                "query_text": "Error logging full query",
                "response_text": "Error occurred",
                "confidence_score": Decimal('0.0'),
                "file_id": str(file_id),
                "timestamp": datetime.utcnow().isoformat()
            }
            table.put_item(Item=minimal_item)
            print(f"✅ Minimal query log saved for debugging")
        except Exception as debug_error:
            print(f"❌ Even minimal logging failed: {debug_error}")