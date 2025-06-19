from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import os

load_dotenv()
app = FastAPI()
'''dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
'''
dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)



@app.get("/metrics/summary")
def get_metrics_summary():
    try:
        table = dynamodb.Table("LLM_Metrics")
        response = table.scan()

        items = response.get("Items", [])
        if not items:
            return {
                "total_queries": 0,
                "avg_response_time": 0,
                "avg_tokens_used": 0,
                "notes": "No metrics available yet"
            }

        total_queries = len(items)
        total_tokens = sum(int(item.get("tokens_used", 0)) for item in items)
        total_response_time = sum(float(item.get("response_time", 0)) for item in items)

        avg_tokens = round(total_tokens / total_queries, 2)
        avg_latency = round(total_response_time / total_queries, 2)

        return {
            "total_queries": total_queries,
            "avg_response_time": avg_latency,
            "avg_tokens_used": avg_tokens
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
