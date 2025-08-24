# from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from fastapi.staticfiles import StaticFiles
# from pathlib import Path
# import uvicorn
# import logging
# from typing import Optional
# import os
# from agents.orchestrator import AgentOrchestrator
# from utils.logging_utils import setup_logging
# from utils.file_utils import save_uploaded_file

# # Initialize logging
# setup_logging()
# logger = logging.getLogger(__name__)

# # FastAPI App Setup
# app = FastAPI(
#     title="SRS-to-App Generator",
#     description="AutoGen-powered backend for converting SRS documents to full-stack apps",
#     version="0.1.0"
# )


# # CORS Configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust for production
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount static files (for generated frontend)
# app.mount("/generated", StaticFiles(directory="output/generated"), name="generated")

# # Global Orchestrator Instance
# orchestrator = AgentOrchestrator()

# @app.on_event("startup")
# async def startup_event():
#     """Initialize resources on startup"""
#     logger.info("Starting up SRS-to-App backend")
#     Path("output/uploaded_files").mkdir(parents=True, exist_ok=True)
#     Path("output/generated").mkdir(parents=True, exist_ok=True)

# # ====================
# # Core API Endpoints
# # ====================

# @app.post("/upload-srs")
# async def upload_srs(
#     file: UploadFile,
#     background_tasks: BackgroundTasks,
#     human_review: Optional[bool] = True
# ):
#     """
#     Upload SRS document and trigger processing pipeline.
#     Returns immediately with task ID, processing continues in background.
#     """
#     try:
#         # Save uploaded file
#         file_path = await save_uploaded_file(file)
        
#         # Configure orchestrator
#         orchestrator.human_in_loop = human_review
        
#         # Start processing in background
#         background_tasks.add_task(
#             orchestrator.execute_workflow,
#             file_path=file_path
#         )
        
#         return {
#             "status": "processing_started",
#             "task_id": orchestrator.current_task_id,
#             "file_path": file_path
#         }
        
#     except Exception as e:
#         logger.error(f"Upload failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/workflow-status/{task_id}")
# def get_workflow_status(task_id: str):
#     """Check status of a running workflow"""
#     if task_id != orchestrator.current_task_id:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     return orchestrator.get_status()

# @app.get("/generated-code")
# def list_generated_artifacts():
#     """List all generated backend/frontend files"""
#     backend_files = []
#     frontend_files = []
    
#     # Scan output directories
#     for path in Path("output/generated/backend").rglob("*"):
#         if path.is_file():
#             backend_files.append(str(path.relative_to("output/generated")))
    
#     for path in Path("output/generated/frontend").rglob("*"):
#         if path.is_file():
#             frontend_files.append(str(path.relative_to("output/generated")))
    
#     return {
#         "backend": backend_files,
#         "frontend": frontend_files
#     }

# # ====================
# # Supporting Endpoints
# # ====================

# @app.get("/health")
# def health_check():
#     """Liveness probe endpoint"""
#     return {"status": "healthy", "version": app.version}

# @app.get("/config")
# def show_config():
#     """Display current configuration (excluding secrets)"""
#     return {
#         "environment": os.getenv("ENV", "development"),
#         "log_level": os.getenv("LOG_LEVEL", "INFO"),
#         "max_file_size": os.getenv("MAX_FILE_SIZE", "10MB")
#     }

# # ====================
# # Error Handlers
# # ====================

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     logger.error(f"HTTP Error: {exc.detail}")
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"error": exc.detail}
#     )

# @app.exception_handler(Exception)
# async def generic_exception_handler(request, exc):
#     logger.critical(f"Unhandled exception: {str(exc)}")
#     return JSONResponse(
#         status_code=500,
#         content={"error": "Internal server error"}
#     )

# # ====================
# # Main Execution
# # ====================

# if __name__ == "__main__":
#     uvicorn.run(
#         app,
#         host="0.0.0.0",
#         port=8000,
#         log_config="config/logging_config.yaml"  # Optional detailed logging
#     )
