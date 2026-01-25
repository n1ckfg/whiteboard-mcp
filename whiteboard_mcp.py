import base64
import os
from datetime import datetime

import cv2
from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI

load_dotenv()
api_key = os.getenv("ZAI_API_KEY")
base_url = os.getenv("ZAI_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)
print([x.id for x in client.models.list()])


mcp = FastMCP(name="WhiteBoardCapture")


def describe_image(
    file_location="./emeet_capture.png",
    prompt="What is in this image? Please give detailed OCR of text and plausible mermaid diagram of any figures drawn please",
):
    with open(file_location, "rb") as image_file:
        b64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.responses.create(
        model="glm-4.6v",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{b64_image}",
                    },
                ],
            }
        ],
    )
    return response.output[0].content[0].text


def capture_webcam(device_index=6, output_file="emeet_capture.png"):
    """Capture a single frame from webcam.

    Args:
        device_index: Webcam device index (default: 0)
        output_file: Output filename (default: webcam_capture_TIMESTAMP.png)
    """
    print(f"📷 Attempting to open webcam at index {device_index}...")

    cap = cv2.VideoCapture(device_index)

    if not cap.isOpened():
        print(f"❌ Failed to open webcam at index {device_index}")
        return False

    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    backend = cap.getBackendName()

    print(f"✅ Webcam opened successfully!")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Backend: {backend}")

    # Read a frame
    print("📸 Capturing frame...")
    ret, frame = cap.read()

    if not ret:
        print("❌ Failed to capture frame")
        cap.release()
        return False

    # Generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"webcam_capture_{timestamp}.png"

    # Save the frame
    print(f"💾 Saving to {output_file}...")
    success = cv2.imwrite(output_file, frame)

    if success:
        print(f"✅ Successfully saved capture to {output_file}")
        print(f"   Image size: {frame.shape[1]}x{frame.shape[0]} pixels")
        print(f"   File size: {len(frame)} bytes (raw)")
    else:
        print(f"❌ Failed to save image to {output_file}")

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
