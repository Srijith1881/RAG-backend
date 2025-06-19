from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, Response
import boto3
import os
import csv
import io
import json
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

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

@app.get("/query-log")
def get_query_logs(limit: int = 10):
    try:
        table = dynamodb.Table("QueryLog")
        response = table.scan(Limit=limit)
        return response.get("Items", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query-log/{file_id}")
def get_logs_for_file(file_id: str):
    try:
        table = dynamodb.Table("QueryLog")
        response = table.scan(
            FilterExpression="file_id = :fid",
            ExpressionAttributeValues={":fid": file_id}
        )
        return response.get("Items", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/query-log/export")
def export_logs(format: str = Query(default="json", enum=["json", "csv"])):
    try:
        table = dynamodb.Table("QueryLog")
        response = table.scan()
        logs = response.get("Items", [])

        if not logs:
            raise HTTPException(status_code=404, detail="No logs found")

        if format == "json":
            return JSONResponse(content=logs)

        elif format == "csv":
            # Convert to CSV string
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=logs[0].keys())
            writer.writeheader()
            writer.writerows(logs)

            return Response(
                content=output.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=query_log.csv"}
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")