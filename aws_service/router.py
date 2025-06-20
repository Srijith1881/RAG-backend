
# receive metrics from the query API

from fastapi import FastAPI
from pydantic import BaseModel
import boto3
import os
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

app = FastAPI()

class Metric(BaseModel):
    run_id: str
    tokens_used: int
    confidence_score: float
    response_time: float
    file_id: str = "unknown"

# AWS Production Configuration (COMMENTED)
# dynamodb = boto3.resource(
#     "dynamodb",
#     region_name=os.getenv("REGION"),
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

@app.post("/metrics")
async def receive_metrics(metric: Metric):
    # Accepts metrics from query response and stores into DynamoDB
    try:
        table = dynamodb.Table("LLM_Metrics")
        
        item = {
            "run_id": metric.run_id,
            "tokens_used": metric.tokens_used,
            "confidence_score": Decimal(str(metric.confidence_score)),
            "response_time": Decimal(str(metric.response_time)),
            "file_id": metric.file_id
        }
        
        table.put_item(Item=item)
        return {"status": "Metric stored."}
    except Exception as e:
        return {"status": "Error", "message": str(e)}