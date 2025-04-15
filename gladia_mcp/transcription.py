"""Transcription functionality for Gladia MCP."""

import asyncio
import logging
from typing import Optional, Dict, Any, BinaryIO
import httpx

from .utils import (
    GLADIA_API_BASE,
    DEFAULT_TIMEOUT,
    get_api_key,
    upload_file,
    poll_result,
)
from .model import TranscriptionResponse

logger = logging.getLogger(__name__)


class TranscriptionClient:
    """Client for handling transcription operations."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize transcription client."""
        self.api_key = api_key or get_api_key()
        self.client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()

    async def transcribe_file(
        self,
        file: BinaryIO,
        filename: str,
        diarization: bool = False,
        language: Optional[str] = None,
        poll_interval: float = 1.0,
    ) -> TranscriptionResponse:
        """
        Transcribe an audio file using Gladia API.

        Args:
            file: File-like object containing audio data
            filename: Name of the file
            diarization: Whether to enable speaker diarization
            language: Optional language code
            poll_interval: Interval between polling attempts in seconds

        Returns:
            TranscriptionResponse object
        """
        # Upload file
        upload_response = await upload_file(file, filename, self.client)
        audio_url = upload_response["audio_url"]

        # Prepare transcription request
        headers = {
            "x-gladia-key": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        data = {"audio_url": audio_url, "diarization": diarization}
        if language:
            data["language"] = language

        # Send transcription request
        response = await self.client.post(
            f"{GLADIA_API_BASE}/pre-recorded/", headers=headers, json=data
        )
        response.raise_for_status()
        post_response = response.json()

        result_url = post_response.get("result_url")
        if not result_url:
            raise ValueError("No result URL in response")

        # Poll for results
        while True:
            poll_response = await poll_result(result_url, self.client)
            status = poll_response.get("status")

            if status == "done":
                return TranscriptionResponse(**poll_response)
            elif status == "error":
                error_response = TranscriptionResponse(
                    status="error",
                    error=str(poll_response.get("error", "Unknown error")),
                )
                return error_response

            await asyncio.sleep(poll_interval)

    async def close(self):
        """Close the client session."""
        await self.client.aclose()
