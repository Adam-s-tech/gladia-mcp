"""Pydantic models for Gladia API responses."""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response from the upload endpoint."""

    audio_url: str = Field(..., description="URL of the uploaded audio file")


class TranscriptionWord(BaseModel):
    """Individual word in the transcription."""

    word: str
    start: float
    end: float
    confidence: float
    speaker: Optional[str] = None


class TranscriptionResult(BaseModel):
    """Complete transcription result."""

    language: str
    text: str
    words: List[TranscriptionWord]
    duration: float
    processing_time: float


class TranscriptionResponse(BaseModel):
    """Response from the transcription endpoint."""

    status: str
    result: Optional[TranscriptionResult] = None
    result_url: Optional[str] = None
    error: Optional[str] = None


class AudioIntelligenceResult(BaseModel):
    """Result from audio intelligence features."""

    feature_type: str
    result: Dict
    processing_time: float


class AudioIntelligenceResponse(BaseModel):
    """Response from audio intelligence endpoints."""

    status: str
    result: Optional[AudioIntelligenceResult] = None
    error: Optional[str] = None
