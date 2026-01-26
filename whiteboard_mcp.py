import base64
import os
import sys
from datetime import datetime

import cv2
from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI

load_dotenv()
# Point to the local Ollama instance
base_url = "http://localhost:11434/v1"
api_key = "ollama"  # required, but unused

client = OpenAI(api_key=api_key, base_url=base_url)

mcp = FastMCP(name="WhiteBoardCapture")


def describe_image(
    file_location="./emeet_capture.png",
    prompt="What is in this image? Please give detailed OCR of text and plausible mermaid diagram of any figures drawn please",
):
    with open(file_location, "rb") as image_file:
        b64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="llava:34b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64_image}"},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content


def capture_webcam(device_index=0, output_file="emeet_capture.png"):
    """Capture a single frame from webcam.

    Args:
        device_index: Webcam device index (default: 0)
        output_file: Output filename (default: webcam_capture_TIMESTAMP.png)
    """
    print(f"📷 Attempting to open webcam at index {device_index}...", file=sys.stderr)

    cap = cv2.VideoCapture(device_index)

    if not cap.isOpened():
        print(f"❌ Failed to open webcam at index {device_index}", file=sys.stderr)
        return False

    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    backend = cap.getBackendName()

    print(f"✅ Webcam opened successfully!", file=sys.stderr)
    print(f"   Resolution: {width}x{height}", file=sys.stderr)
    print(f"   FPS: {fps}", file=sys.stderr)
    print(f"   Backend: {backend}", file=sys.stderr)

    # Read a frame
    print("📸 Capturing frame...", file=sys.stderr)
    ret, frame = cap.read()

    if not ret:
        print("❌ Failed to capture frame", file=sys.stderr)
        cap.release()
        return False

    # Generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"webcam_capture_{timestamp}.png"

    # Save the frame
    print(f"💾 Saving to {output_file}...", file=sys.stderr)
    success = cv2.imwrite(output_file, frame)

    if success:
        print(f"✅ Successfully saved capture to {output_file}", file=sys.stderr)
        print(f"   Image size: {frame.shape[1]}x{frame.shape[0]} pixels", file=sys.stderr)
        print(f"   File size: {len(frame)} bytes (raw)", file=sys.stderr)
    else:
        print(f"❌ Failed to save image to {output_file}", file=sys.stderr)

    cap.release()
    return success


@mcp.tool
def capture_whiteboard(
    prompt: str = "What is in this image? Please give detailed OCR of text, mathematical expressions, and plausible mermaid diagram of any figures drawn please",
):
    """Capture a whiteboard image and analyze it with AI.

    Args:
        prompt: Optional[str] - The prompt to use for analyzing the captured image. If default it will use a generic math enabled OCR + mermaid diagram extracting prompt.
    """
    output_file = "./emeet_capture.png"
    capture_webcam(output_file=output_file)
    description = describe_image(file_location=output_file, prompt=prompt)
    os.remove(output_file)
    return description


if __name__ == "__main__":
    mcp.run(transport="stdio")
