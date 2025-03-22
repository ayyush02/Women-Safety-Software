import cv2
import time

def initialize_camera():
    global cap
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No available camera found! Exiting...")
        exit(1)

    # Release the camera and reinitialize
    cap.release()
    time.sleep(2)  # Wait for 2 seconds before reinitializing
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        print("✅ Camera successfully reinitialized!")
    else:
        print("❌ Camera failed to open after reinitialization!")

initialize_camera()
