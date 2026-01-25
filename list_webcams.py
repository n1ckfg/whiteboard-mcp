#!/usr/bin/env python3
"""List all available webcams using OpenCV."""

import cv2
import os

def get_video_devices():
    """Get list of video devices from /dev using udevadm."""
    video_devices = []
    try:
        for i in range(10):
            device_path = f"/dev/video{i}"
            if os.path.exists(device_path):
                # Try to get device info using udevadm
                try:
                    result = os.popen(f'udevadm info --query=property --name="{device_path}" 2>/dev/null | grep -E "^(ID_MODEL|ID_VENDOR)=" | sed "s/^ID_\\(MODEL\\|VENDOR\\)=//"').read()
                    lines = result.strip().split('\n')
                    if len(lines) >= 2:
                        # Clean up the vendor and model names (replace underscores with spaces)
                        vendor = lines[0].replace('_', ' ')
                        model = lines[1].replace('_', ' ')
                        card_type = f"{vendor} {model}"
                    else:
                        card_type = "Unknown"
                except:
                    card_type = "Unknown"
                
                video_devices.append({
                    'index': i,
                    'path': device_path,
                    'name': card_type
                })
    except Exception as e:
        print(f"Warning: Could not query video devices: {e}")
    
    return video_devices

def list_webcams():
    """Test webcam indices from 0-10 to find available devices."""
    print("🔍 Scanning for available webcams...\n")
    
    # First, get video device info
    video_devices = get_video_devices()
    device_map = {d['index']: d for d in video_devices}
    
    available_webcams = []
    
    # Test indices 0-10 (most systems don't have more than 10 webcams)
    for index in range(11):
        cap = cv2.VideoCapture(index)
        
        if cap.isOpened():
            # Try to read a frame to make sure it actually works
            ret, frame = cap.read()
            
            if ret:
                # Get webcam properties
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                backend = cap.getBackendName()
                
                # Get device name if available
                device_name = device_map.get(index, {}).get('name', 'Unknown')
                
                available_webcams.append({
                    'index': index,
                    'width': width,
                    'height': height,
                    'fps': fps,
                    'backend': backend,
                    'device_name': device_name
                })
                
                print(f"✅ Webcam {index}:")
                print(f"   Device: {device_name}")
                print(f"   Resolution: {width}x{height}")
                print(f"   FPS: {fps}")
                print(f"   Backend: {backend}")
                print()
            
            cap.release()
    
    if not available_webcams:
        print("❌ No webcams found!")
        print("\nTroubleshooting tips:")
        print("  • Check if the webcam is connected")
        print("  • Check permissions: ls -l /dev/video*")
        print("  • Try running with sudo")
        print("  • Make sure no other application is using the webcam")
    else:
        print(f"📷 Found {len(available_webcams)} webcam(s)!")
        print("\nRecommended usage:")
        for cam in available_webcams:
            print(f"  cv2.VideoCapture({cam['index']})  # {cam['device_name']} - {cam['width']}x{cam['height']} @ {cam['backend']}")
    
    return available_webcams

if __name__ == "__main__":
    list_webcams()
