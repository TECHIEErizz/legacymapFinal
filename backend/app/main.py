"""FastAPI main application for LegacyMap backend."""

import os
import uuid
from typing import Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile

from .scanner import CodeScanner
from .ai_summary import generate_summary


# Create FastAPI app
app = FastAPI(
    title="LegacyMap API",
    description="Code analysis and dependency mapping API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store analysis results in memory (in production, use a database)
analysis_cache: Dict[str, Dict[str, Any]] = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LegacyMap API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/upload-analyze")
async def upload_and_analyze(file: UploadFile = File(...)):
    """
    Upload a ZIP file and analyze the code.
    
    Args:
        file: ZIP file containing code to analyze
    
    Returns:
        Analysis results including files, functions, and dependencies
    """
    # Validate file type
    if not file.filename.endswith('.zip'):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are supported"
        )
    
    # Save uploaded file to temp location
    temp_file = None
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Analyze the ZIP file
        scanner = CodeScanner()
        results = scanner.analyze_zip(temp_file_path)
        
        # Generate unique repo ID
        repo_id = str(uuid.uuid4())
        
        # Cache results
        analysis_cache[repo_id] = results
        
        # Add repo_id to response
        results["repo_id"] = repo_id
        
        return JSONResponse(content=results)
    
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=400,
            detail="Invalid ZIP file"
        )
    except Exception as e:
        print(f"Error analyzing file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing file: {str(e)}"
        )
    
    finally:
        # Cleanup temp file
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass


@app.get("/function-details/{repo_id}/{file_path:path}/{function_name}")
async def get_function_details(repo_id: str, file_path: str, function_name: str):
    """
    Get detailed information about a specific function.
    
    Args:
        repo_id: Repository ID from analysis
        file_path: Path to file containing the function
        function_name: Name of the function
    
    Returns:
        Function details including call sites and dependencies
    """
    # Get cached analysis
    if repo_id not in analysis_cache:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found. Please upload and analyze the code first."
        )
    
    analysis = analysis_cache[repo_id]
    files_data = analysis.get("files", [])
    
    # Create scanner to get function details
    scanner = CodeScanner()
    details = scanner.get_function_details(files_data, file_path, function_name)
    
    if not details:
        raise HTTPException(
            status_code=404,
            detail=f"Function '{function_name}' not found in file '{file_path}'"
        )
    
    return JSONResponse(content=details)


@app.get("/analysis/{repo_id}")
async def get_analysis(repo_id: str):
    """
    Get cached analysis results.
    
    Args:
        repo_id: Repository ID from previous analysis
    
    Returns:
        Analysis results
    """
    if repo_id not in analysis_cache:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )
    
    return JSONResponse(content=analysis_cache[repo_id])


@app.delete("/analysis/{repo_id}")
async def delete_analysis(repo_id: str):
    """Delete analysis results."""
    if repo_id in analysis_cache:
        del analysis_cache[repo_id]
        return {"message": "Analysis deleted"}
    raise HTTPException(status_code=404, detail="Analysis not found")


@app.post("/generate-summary/{repo_id}")
async def get_ai_summary(repo_id: str):
    """Generate an AI summary for a specific analysis."""
    if repo_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis_data = analysis_cache[repo_id]
    summary = generate_summary(analysis_data)
    return {"summary": summary}


# Import zipfile for error handling
import zipfile


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
