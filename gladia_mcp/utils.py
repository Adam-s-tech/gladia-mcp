"""Utility functions for Gladia MCP."""

import os
import logging
from typing import Optional, Dict, Any, BinaryIO
from pathlib import Path
import mimetypes
import httpx

logger = logging.getLogger(__name__)

GLADIA_API_BASE = "https://api.gladia.io/v2"
DEFAULT_TIMEOUT = 30.0


def get_api_key() -> str:
    """Get Gladia API key from environment."""
    api_key = os.getenv("GLADIA_API_KEY")
    if not api_key:
        raise ValueError("GLADIA_API_KEY environment variable not set")
    return api_key


def get_mime_type(file_path: str) -> str:
    """Get MIME type for a file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("audio/"):
        return "audio/wav"  # Default to wav if unknown
    return mime_type


async def upload_file(
    file: BinaryIO, filename: str, client: httpx.AsyncClient
) -> Dict[str, Any]:
    """Upload a file to Gladia API."""
    headers = {
        "x-gladia-key": get_api_key(),
        "accept": "application/json",
    }

    files = {"audio": (filename, file, get_mime_type(filename))}

    response = await client.post(
        f"{GLADIA_API_BASE}/upload/",
        headers=headers,
        files=files,
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


async def poll_result(result_url: str, client: httpx.AsyncClient) -> Dict[str, Any]:
    """Poll for result from Gladia API."""
    headers = {
        "x-gladia-key": get_api_key(),
        "accept": "application/json",
    }

    response = await client.get(result_url, headers=headers, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def validate_audio_file(file_path: str) -> None:
    """Validate audio file exists and is accessible."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Cannot read file: {file_path}")


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
