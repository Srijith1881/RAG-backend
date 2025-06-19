import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()
lambda_client = boto3.client(
    "lambda",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

'''lambda_client = boto3.client(
    "lambda",
    endpoint_url="http://localhost:4566",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)'''

bucket = "pdf-storage"

def send_metrics(run_id, tokens_used, confidence, response_time, file_id="unknown"):
    payload = {
        "run_id": run_id,
        "tokens_used": tokens_used,
        "confidence_score": confidence,
        "response_time": response_time,
        "file_id": file_id
    }

    try:
        response = lambda_client.invoke(
            FunctionName="logMetricsFunction",
            InvocationType="Event",
            Payload=json.dumps(payload)
        )
        print("✅ Metrics sent to AWS Lambda.")
    except Exception as e:
        print(f"❌ Failed to send metrics to AWS Lambda: {e}")

