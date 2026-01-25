#!/usr/bin/env python3
"""Test capturing from webcam using direct device path."""

import cv2
import sys

def test_device_path(device_path):
    """Test opening a webcam using its device path."""
    print(f"📷 Attempting to open {device_path}...")
    
    # Try with V4L2 backend explicitly
    cap = cv2.VideoCapture(device_path, cv2.CAP_V4L2)
    
    if not cap.isOpened():
        print(f"❌ Failed to open {device_path}")
        return False
    
    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"✅ Opened successfully!")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    
    # Set to higher resolution if available
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"   After setting: {width}x{height}")
    
    # Read a frame
    print("📸 Capturing frame...")
    ret, frame = cap.read()
    
    if not ret:
        print("❌ Failed to capture frame")
        cap.release()
        return False
    
    print(f"✅ Captured frame: {frame.shape[1]}x{frame.shape[0]}")
    
    # Save it
    output_file = "test_direct_capture.png"
    success = cv2.imwrite(output_file, frame)
    
    if success:
        print(f"✅ Saved to {output_file}")
    else:
        print(f"❌ Failed to save")
    
    cap.release()
    return success

if __name__ == "__main__":
    device_path = sys.argv[1] if len(sys.argv) > 1 else "/dev/video0"
    test_device_path(device_path)
