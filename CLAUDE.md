# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Start the application:**
```bash
python app.py
```

**Using virtual environment:**
```bash
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Docker commands:**
```bash
# Build image
docker build -t ilab-client .

# Run container
docker run -d -p 5000:5000 --name ilab-client ilab-client

# Run with custom AI service address
docker run -d -p 5000:5000 -e ADDRESS="http://api.your-aiservice.com" --name ilab-client ilab-client
```

## Architecture

This is a Flask web application that serves as a client interface for interacting with an AI language model API. The application has two main components:

1. **Web Interface** (`templates/index.html`): A single-page application using Tailwind CSS that provides a question/answer interface
2. **API Proxy** (`app.py`): Flask server that proxies requests to an external AI service at `/v1/completions`

**Key architectural details:**
- The app proxies requests to an AI service specified by the `ADDRESS` environment variable (defaults to `http://127.0.0.1:8000`)
- API endpoint `/api/completions` accepts POST requests with `{"question": "text"}` and forwards them to the AI service as completion requests
- The AI service is expected to follow OpenAI-compatible API format with `/v1/completions` endpoint
- Responses are extracted from `choices[0].text` in the AI service response

**Environment Configuration:**
- `ADDRESS`: URL of the AI language model API (automatically prefixed with `http://` if no scheme provided)
- Application runs on `0.0.0.0:5000` by default

## Git Workflow

Use conventional git flow with one line commits following the format:
```
type(scope): description
```

Examples:
- `feat: add user authentication`
- `fix: resolve timeout issue in API calls`
- `docs: update README installation steps`
- `refactor: simplify error handling logic`