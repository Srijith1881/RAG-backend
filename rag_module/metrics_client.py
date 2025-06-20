# Send metrices for either AWS lambda or Localstack

import boto3
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# AWS Lambda Configuration (COMMENTED)
# lambda_client = boto3.client(
#     "lambda",
#     region_name=os.getenv("REGION"),
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
# )

# def send_metrics(run_id, tokens_used, confidence, response_time, file_id="unknown"):
#     payload = {
#         "run_id": run_id,
#         "tokens_used": tokens_used,
#         "confidence_score": confidence,
#         "response_time": response_time,
#         "file_id": file_id
#     }
#     try:
#         response = lambda_client.invoke(
#             FunctionName="logMetricsFunction",
#             InvocationType="Event",
#             Payload=json.dumps(payload)
#         )
#         print("✅ Metrics sent to AWS Lambda.")
#     except Exception as e:
#         print(f"❌ Failed to send metrics to AWS Lambda: {e}")

# LocalStack Configuration - Direct HTTP call to metrics service
def send_metrics(run_id, tokens_used, confidence, response_time, file_id="unknown"):
    endpoint = "http://localhost:8003/metrics"
    payload = {
        "run_id": run_id,
        "tokens_used": tokens_used,
        "confidence_score": confidence,
        "response_time": response_time,
        "file_id": file_id
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        print("✅ Metrics sent to local metrics service.")
    except Exception as e:
        print(f"❌ Failed to send metrics: {e}")