from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rag_module.rag_chain import get_vectorstore, create_chain_from_retriever
from rag_module.metrics_client import send_metrics
import os, time, uuid, traceback

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query(request: Request):
    try:
        data = await request.json()
        question = data.get("query", "").strip()

        if not question:
            raise HTTPException(status_code=400, detail="Empty query.")

        # ✅ Load vector store and retrieve
        vectorstore = get_vectorstore()
        retriever = vectorstore.as_retriever()
        chain = create_chain_from_retriever(retriever)

        run_id = str(uuid.uuid4())
        start = time.time()
        result = chain.invoke(question)
        latency = time.time() - start

        send_metrics(run_id, tokens_used=345, confidence=0.92, response_time=latency)

        return {"run_id": run_id, "reply": result}

    except HTTPException as he:
        raise he
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
