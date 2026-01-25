#!/usr/bin/env python3
"""Capture a single frame from webcam and save to file."""

import sys
from datetime import datetime

import cv2


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


if __name__ == "__main__":
    # Use first command line arg as device index, default to 0
    device_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    # Use second command line arg as output filename, optional
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    capture_webcam(device_index, output_file)
