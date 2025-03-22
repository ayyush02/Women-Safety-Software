import cv2
import numpy as np
import subprocess
import time
import os
import requests
from twilio.rest import Client

# Twilio Credentials
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number
RECIPIENT_WHATSAPP_NUMBER = "whatsapp:+your_number"

# Node.js Server URL
NODE_SERVER_URL = "http://your-server-ip:port/upload"

# Parameters
duration = 10  # Duration per video
frame_width, frame_height = 640, 480  # Video resolution
video_fps = 20  # Frames per second

# Create folders
os.makedirs("Videos", exist_ok=True)
os.makedirs("Images", exist_ok=True)

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, frame_width)  # Set width
cap.set(4, frame_height)  # Set height

def record_video():
    timestamp = int(time.time())
    video_filename = f"Videos/video_{timestamp}.mp4"
    image_filename = f"Images/image_{timestamp}.jpg"

    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_filename, fourcc, video_fps, (frame_width, frame_height))

    start_time = time.time()
    print(f"Recording video: {video_filename}")

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

        # Capture image in the middle of recording
        if int(time.time() - start_time) == duration // 2:
            cv2.imwrite(image_filename, frame)
            print(f"Image captured: {image_filename}")

        cv2.imshow("Recording", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    print(f"Video saved: {video_filename}")

    return video_filename, image_filename

# Function to send video and image to server
def send_to_server(video_path, image_path):
    files = {
        'video': open(video_path, 'rb'),
        'image': open(image_path, 'rb')
    }
    response = requests.post(NODE_SERVER_URL, files=files)

    if response.status_code == 200:
        print("Video and image successfully uploaded to server.")
    else:
        print(f"Failed to upload. Server response: {response.text}")

# Function to send video and image via WhatsApp
def send_whatsapp(video_path, image_path):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Send image
    image_message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=RECIPIENT_WHATSAPP_NUMBER,
        body="Captured Image",
        media_url=f"https://your-server.com/images/{os.path.basename(image_path)}"
    )
    print(f"WhatsApp Image Sent: {image_message.sid}")

    # Send video
    video_message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=RECIPIENT_WHATSAPP_NUMBER,
        body="Recorded Video",
        media_url=f"https://your-server.com/videos/{os.path.basename(video_path)}"
    )
    print(f"WhatsApp Video Sent: {video_message.sid}")

# Start recording
video_file, image_file = record_video()

# Send to backend
send_to_server(video_file, image_file)

# Send to WhatsApp
send_whatsapp(video_file, image_file)

cap.release()
cv2.destroyAllWindows()
