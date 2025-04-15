# Gladia MCP

<div class="title-block" style="text-align: center;" align="center">

  [![PyPI](https://img.shields.io/badge/PyPI-gladia--mcp-000000.svg?style=for-the-badge&logo=pypi&labelColor=000)](https://pypi.org/project/gladia-mcp)
  [![Tests](https://img.shields.io/badge/tests-passing-000000.svg?style=for-the-badge&logo=github&labelColor=000)](https://github.com/gladia/gladia-mcp/actions/workflows/test.yml)

</div>

<p align="center">
  Official Gladia <a href="https://github.com/modelcontextprotocol">Model Context Protocol (MCP)</a> server that enables interaction with powerful Speech-to-Text and Audio Intelligence APIs. This server allows MCP clients like <a href="https://www.anthropic.com/claude">Claude Desktop</a>, <a href="https://www.cursor.so">Cursor</a>, <a href="https://codeium.com/windsurf">Windsurf</a>, <a href="https://github.com/openai/openai-agents-python">OpenAI Agents</a> and others to transcribe audio, analyze speech, translate content, and more.
</p>

## Features

- Audio transcription with speaker diarization
- Real-time speech-to-text
- Audio intelligence capabilities:
  - Translation
  - Summarization
  - Named Entity Recognition
  - Sentiment Analysis
  - Content Moderation
  - Chapterization
  - Audio to LLM integration
- Async API with FastAPI
- Easy-to-use CLI interface
- Configurable logging
- CORS support
- Health check endpoint

## Quickstart with Claude Desktop

1. Get your API key from [Gladia](https://app.gladia.io/settings/api-keys). There is a free tier available.
2. Install `uv` (Python package manager), install with `curl -LsSf https://astral.sh/uv/install.sh | sh` or see the `uv` [repo](https://github.com/astral-sh/uv) for additional install methods.
3. Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:

```json
{
  "mcpServers": {
    "Gladia": {
      "command": "uvx",
      "args": ["gladia-mcp"],
      "env": {
        "GLADIA_API_KEY": "<insert-your-api-key-here>"
      }
    }
  }
}
```

If you're using Windows, you will have to enable "Developer Mode" in Claude Desktop to use the MCP server. Click "Help" in the hamburger menu at the top left and select "Enable Developer Mode".

## Other MCP clients

For other clients like Cursor and Windsurf, run:
1. `pip install gladia-mcp`
2. `python -m gladia_mcp --api-key={{PUT_YOUR_API_KEY_HERE}} --print` to get the configuration. Paste it into appropriate configuration directory specified by your MCP client.

## Example usage

Try asking Claude:

- "Transcribe this audio file and identify different speakers"
- "Convert this recording to text and translate it to Spanish"
- "Analyze the sentiment and emotions in this speech"
- "Extract key topics and create chapters from this long audio file"
- "Transcribe this conversation and summarize the main points"

## Optional features

You can add the `GLADIA_MCP_BASE_PATH` environment variable to the `claude_desktop_config.json` to specify the base path MCP server should look for and output files specified with relative paths.

## Contributing

If you want to contribute or run from source:

1. Clone the repository:
```bash
git clone https://github.com/gladia/gladia-mcp
cd gladia-mcp
```

2. Create a virtual environment and install dependencies [using uv](https://github.com/astral-sh/uv):
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

3. Copy `.env.example` to `.env` and add your Gladia API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

4. Run the tests to make sure everything is working:
```bash
./scripts/test.sh
# Or with options
./scripts/test.sh --verbose --fail-fast
```

5. Install the server in Claude Desktop: `mcp install gladia_mcp/server.py`

6. Debug and test locally with MCP Inspector: `mcp dev gladia_mcp/server.py`

## API Endpoints

### Health Check
```
GET /health
```

### Transcribe Audio
```
POST /transcribe
```

Parameters:
- `file`: Audio file (multipart/form-data)
- `diarization`: Enable speaker diarization (boolean, optional)
- `language`: Language code (string, optional)

Example using curl:
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav" \
  -F "diarization=true"
```

## Troubleshooting

Logs when running with Claude Desktop can be found at:
- **Windows**: `%APPDATA%\Claude\logs\mcp-server-gladia.log`
- **macOS**: `~/Library/Logs/Claude/mcp-server-gladia.log`

### MCP Gladia: spawn uvx ENOENT

If you encounter the error "MCP Gladia: spawn uvx ENOENT", confirm its absolute path by running this command in your terminal:
```bash
which uvx
```

Once you obtain the absolute path (e.g., `/usr/local/bin/uvx`), update your configuration to use that path (e.g., `"command": "/usr/local/bin/uvx"`). This ensures that the correct executable is referenced.

## Development

### Running Tests
```bash
pytest
```

### Code Style
The project follows PEP 8 style guide. Use flake8 for linting:
```bash
flake8 gladia_mcp
```

## License

MIT License



