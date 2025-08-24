"""
FastAPI endpoints for multi-agent requirements analysis workflow
with integrated parser and logger.
"""
import os
import tempfile
import shutil
import asyncio

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.parser import parse_doc_file
from utils.logging_utils import setup_logger
from config.settings import config 
from config.settings import FOLDER_PATH
from agents.orchestrator_agent import analyze_requirements

logger = setup_logger("backend", config.LOG_DIR)

app = FastAPI(
    title="Multi-Agent Requirements Analyzer",
    description="Upload requirements docs, get frontend/backend SRDs (Markdown).",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    logger.info("Health check endpoint called.")
    return {"status": "ok"}

@app.post("/analyze-requirements")
async def analyze_requirements_endpoint(
    doc1: UploadFile = File(..., description="First requirements document (PDF, DOCX, MD, TXT)"),
    doc2: UploadFile = File(..., description="Second requirements document (PDF, DOCX, MD, TXT)")
):
    """
    Accepts two requirements documents, parses them, runs the agent workflow,
    and returns the generated SRDs as Markdown.
    """
    logger.info("Received request to analyze requirements with two documents.")

    try:
        text1 = parse_doc_file(doc1)
        logger.info(f"Parsed first document. Length: {len(text1)} characters.")

        text2 = parse_doc_file(doc2)
        logger.info(f"Parsed second document. Length: {len(text2)} characters.")
        
        combined_requirements = f"{text1}\n\n{text2}"
        logger.info("Combined both documents for agent analysis.")
    except Exception as e:
        logger.error(f"File parsing failed: {e}")
        raise HTTPException(status_code=400, detail=f"File parsing failed: {e}")
    finally:
        if 'tmp1_path' in locals() and os.path.exists(doc1):
            os.remove(doc1)
        if 'tmp2_path' in locals() and os.path.exists(doc2):
            os.remove(doc2)

  
    try:
        logger.info("Starting agent workflow for requirements analysis.")
        await analyze_requirements(combined_requirements)
        logger.info("Agent workflow completed.")
    except Exception as e:
        logger.error(f"Agent workflow failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent workflow failed: {e}")

 
    folder_path = os.getenv("FOLDER_PATH", config.OUTPUT_DIR)
    frontend_md_path = os.path.join(folder_path, "srd_frontend.md")
    backend_md_path = os.path.join(folder_path, "srd_backend.md")

    if not (os.path.exists(frontend_md_path) and os.path.exists(backend_md_path)):
        logger.error("SRD markdown files not generated.")
        raise HTTPException(status_code=500, detail="SRD markdown files not generated.")

    with open(frontend_md_path, "r", encoding="utf-8") as f:
        frontend_md = f.read()
    with open(backend_md_path, "r", encoding="utf-8") as f:
        backend_md = f.read()

    logger.info("Returning generated SRDs to client.")

    return JSONResponse({
        "frontend_srd_md": frontend_md,
        "backend_srd_md": backend_md,
        "frontend_srd_file": frontend_md_path,
        "backend_srd_file": backend_md_path
    })

@app.get("/download-srd/{which}")
def download_srd(which: str):
    """
    Download the generated SRD markdown file.
    """
    folder_path = FOLDER_PATH
    if which == "frontend":
        file_path = os.path.join(folder_path, "srd_frontend.md")
    elif which == "backend":
        file_path = os.path.join(folder_path, "srd_backend.md")
    else:
        logger.error(f"Unknown SRD type requested: {which}")
        raise HTTPException(status_code=404, detail="Unknown SRD type.")
    if not os.path.exists(file_path):
        logger.error(f"Requested SRD file not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found.")
    logger.info(f"Serving SRD file: {file_path}")
    return FileResponse(file_path, media_type="text/markdown", filename=os.path.basename(file_path))

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/download-zip/{zip_filename}")
def download_zip(zip_filename: str):
    # Security: Only allow .zip files and prevent path traversal
    if not zip_filename.endswith(".zip") or "/" in zip_filename or "\\" in zip_filename:
        raise HTTPException(status_code=400, detail="Invalid file name.")
    zip_path = os.path.join(PROJECT_DIR, zip_filename)
    if not os.path.isfile(zip_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(
        path=zip_path,
        filename=zip_filename,
        media_type="application/zip"
    )