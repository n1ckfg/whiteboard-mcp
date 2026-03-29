# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

whiteboard-mcp is an MCP (Model Context Protocol) server that captures images from a webcam and analyzes them using a Vision Language Model (VLM). It's designed for capturing whiteboards and extracting text (OCR), mathematical expressions, and diagrams (as mermaid syntax).

## Commands

**Run the MCP server:**
```bash
uv --project /path/to/whiteboard-mcp run whiteboard_mcp.py
```

**List available webcams:**
```bash
uv run list_webcams.py
```

**Test webcam capture:**
```bash
uv run capture_webcam.py <device_index> [output_file]
```

**Test device path directly (Linux V4L2):**
```bash
uv run test_direct_device.py /dev/video0
```

## Architecture

The server uses FastMCP to expose a single tool `capture_whiteboard` that:
1. Captures a frame from a configured webcam using OpenCV
2. Sends the image to a VLM API (configured via `ZAI_API_KEY` and `ZAI_BASE_URL` env vars)
3. Returns the VLM's analysis (OCR text, math expressions, mermaid diagrams)

**Key configuration:** The `device_index` in `capture_webcam()` (default: 6) must be set to match your webcam. Use `list_webcams.py` to find the correct index.

## Environment Variables

- `ZAI_API_KEY` - API key for the VLM service
- `ZAI_BASE_URL` - Base URL for the VLM API endpoint

## Dependencies

Uses `uv` for dependency management. Key dependencies: `fastmcp`, `opencv-python`, `openai` (for API client), `pillow`.
