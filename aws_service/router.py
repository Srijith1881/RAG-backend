from fastapi import FastAPI
from pydantic import BaseModel
import boto3

app = FastAPI()

class Metric(BaseModel):
    run_id: str
    tokens_used: int
    confidence_score: float
    response_time: float

@app.post("/metrics")
async def receive_metrics(metric: Metric):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566")
    table = dynamodb.Table("LLM_Metrics")
    table.put_item(Item=metric.dict())
    return {"status": "Metric stored."}
