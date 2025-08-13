from __future__ import annotations

import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.rag.pipeline import RagAnalyzer
from app.rag.schemas import AnalyzeResponse, ErrorResponse

app = FastAPI(title="Research Paper RAG Agent", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/analyze", response_model=AnalyzeResponse, responses={400: {"model": ErrorResponse}})
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse(status_code=400, content={"ok": False, "error": "Only PDF files are supported"})

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp.flush()
            tmp_path = tmp.name

        analyzer = RagAnalyzer()
        result = analyzer.analyze(tmp_path)
        return {"ok": True, "result": result}
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})
    finally:
        try:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass