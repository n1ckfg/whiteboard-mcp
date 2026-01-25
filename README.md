<p align="center">
    <img src="https://github.com/odellus/crow/raw/v0.1.0/assets/crow-logo-crop.png" description="crow logo"width=500/>
</p>

# whiteboard-mcp

A simple MCP server for webcam capture of whiteboards and VLM analysis

## Installation

clone this repo 
```
git clone https://github.com/odellus/whiteboard-mcp.git
cd whiteboard-mcp
```

Use `list_webcams.py` and `capture_webcam.py` to determine which webcam to use to capture the whiteboard.

Once you have it figured out change the `webcam_id` variable in `whiteboard_mcp.py` to the id of the webcam you want to use.


## Configure clients

In zed 

```json
{"context_servers": {
    "whiteboard": {
      "enabled": true,
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/webcam-mcp",
        "/path/to/webcam-mcp/whiteboard_mcp.py",
      ],
      "env": {},
    },
  },
}
```
