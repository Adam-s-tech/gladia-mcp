"""Command line interface for Gladia MCP."""

import os
import sys
import argparse
import asyncio
import uvicorn
from pathlib import Path

from .utils import setup_logging
from . import __version__


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Gladia Media Control Protocol Server")

    parser.add_argument(
        "--version", action="version", version=f"Gladia MCP v{__version__}"
    )

    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to bind server to"
    )

    parser.add_argument("--port", type=int, default=8000, help="Port to bind server to")

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )

    return parser.parse_args()


def validate_environment():
    """Validate required environment variables."""
    if not os.getenv("GLADIA_API_KEY"):
        print("Error: GLADIA_API_KEY environment variable not set")
        print("Please set your Gladia API key:")
        print("export GLADIA_API_KEY='your-api-key'")
        sys.exit(1)


def main():
    """Main entry point."""
    args = parse_args()

    # Setup logging
    setup_logging(args.log_level)

    # Validate environment
    validate_environment()

    # Start server
    uvicorn.run(
        "gladia_mcp.server:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level.lower(),
        reload=True,
    )


if __name__ == "__main__":
    main()
