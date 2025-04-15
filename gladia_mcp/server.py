"""FastAPI server for Gladia MCP."""

import logging
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import httpx

from .transcription import TranscriptionClient
from .model import TranscriptionResponse
from .utils import setup_logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gladia MCP",
    description="Gladia Media Control Protocol Server",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
setup_logging()


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    app.state.http_client = httpx.AsyncClient()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown."""
    await app.state.http_client.aclose()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    diarization: bool = False,
    language: Optional[str] = None,
):
    """
    Transcribe an audio file.

    Args:
        file: Audio file to transcribe
        diarization: Enable speaker diarization
        language: Optional language code

    Returns:
        TranscriptionResponse object
    """
    try:
        async with TranscriptionClient() as client:
            response = await client.transcribe_file(
                file.file, file.filename, diarization=diarization, language=language
            )
            return response
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
