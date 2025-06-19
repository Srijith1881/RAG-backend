from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid, os, shutil
from pdf_services.processor import extract_text
from aws_service.s3_handler import upload_to_s3
from aws_service.dynamo_handler import save_metadata
from rag_module.indexing import index_document
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
from aws_service.dynamo_handler import get_metadata, list_metadata

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from fastapi import HTTPException

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        file_id = str(uuid.uuid4())
        filename = f"{file_id}.pdf"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        upload_to_s3(file_path, filename)
        docs = extract_text(file_path)
        save_metadata(file_id=file_id, filename=file.filename)
        index_document(docs)

        return {"file_id": file_id, "message": "Uploaded and indexed successfully"}

    except HTTPException as http_exc:
        # ✅ Re-raise actual HTTPExceptions without masking them
        raise http_exc

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/retrieve/{file_id}")
def retrieve_file_metadata(file_id: str):
    try:
        metadata = get_metadata(file_id)
        if metadata:
            return metadata
        raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list")
def list_files(page: int = 1, limit: int = 10):
    try:
        all_items = list_metadata()
        start = (page - 1) * limit
        end = start + limit
        return {
            "total": len(all_items),
            "page": page,
            "limit": limit,
            "files": all_items[start:end]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))