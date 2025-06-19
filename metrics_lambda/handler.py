import boto3
import os
import json
from decimal import Decimal
from dotenv import load_dotenv
import botocore.exceptions

load_dotenv()

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def lambda_handler(event, context):
    try:
        table = dynamodb.Table("LLM_Metrics")

        # Parse input from API Gateway or Lambda test event
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        item = {
            "run_id": body["run_id"],
            "tokens_used": body["tokens_used"],
            "confidence_score": Decimal(str(body["confidence_score"])),
            "response_time": Decimal(str(body["response_time"]))
        }

        table.put_item(Item=item)
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "Metric stored."})
        }

    except botocore.exceptions.ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"DynamoDB error: {str(e)}"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Unexpected error: {str(e)}"})
        }
