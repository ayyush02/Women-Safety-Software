import cv2
import sounddevice as sd
import numpy as np
import wave
import time
import os
import threading
import requests

# Backend server details
BACKEND_URL = "http://192.168.43.40:3000/send-mail"  # Change to your backend IP and port

# Parameters
duration = 10  # Duration per video/audio in seconds
sample_rate = 44100  # Audio sample rate
channels = 2  # Stereo audio
frame_width, frame_height = 640, 480  # Video resolution
video_fps = 20  # Frames per second for video

# Create necessary folders
os.makedirs("Audio", exist_ok=True)
os.makedirs("Videos", exist_ok=True)

# Function to initialize the camera safely
def initialize_camera():
    global cap
    for i in range(3):  # Try camera indexes 0, 1, 2
        print(f"🔄 Attempting to initialize camera at index {i}")
        cap = cv2.VideoCapture(i)
        cap.set(3, frame_width)
        cap.set(4, frame_height)
        if cap.isOpened():
            print(f"✅ Camera initialized at index {i}")
            return
        else:
            print(f"❌ Failed to initialize camera at index {i}")
    print("❌ Camera not found! Exiting...")
    exit(1)

# Initialize camera
initialize_camera()

# Function to send file to backend
def send_to_backend(file_path, file_type):
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempting to upload {file_type}: {file_path} to {BACKEND_URL} (Attempt {attempt + 1}/{max_retries})")
            with open(file_path, "rb") as f:
                if file_type == "video":
                    files = {"video": (file_path, f)}
                elif file_type == "audio":
                    files = {"audio": (file_path, f)}
                else:
                    print(f"❌ Unsupported file type: {file_type}")
                    return

                data = {"type": file_type}

                # Try sending the file with a 10-second timeout
                response = requests.post(BACKEND_URL, files=files, data=data, timeout=10)

                if response.status_code == 200:
                    print(f"✅ Uploaded {file_type}: {file_path}")
                    return
                else:
                    print(f"⚠ Failed to upload {file_type}: {file_path} - Server responded with: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error uploading {file_type}: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"❌ Failed to upload {file_type} after {max_retries} attempts")

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return

        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            return

# Function to record audio
def record_audio(audio_file):
    print(f"🎙 Recording audio: {audio_file}")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()

    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"✅ Audio saved: {audio_file}")
    send_to_backend(audio_file, "audio")  # Send audio to backend

# Function to record continuous video with audio
def record_continuous():
    while True:
        timestamp = int(time.time())
        video_filename = f"Videos/video_{timestamp}.mp4"
        audio_filename = f"Audio/audio_{timestamp}.wav"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_filename, fourcc, video_fps, (frame_width, frame_height))

        start_time = time.time()

        # Start audio recording in a separate thread
        audio_thread = threading.Thread(target=record_audio, args=(audio_filename,))
        audio_thread.start()

        print(f"🎥 Recording new video: {video_filename}")

        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()
        audio_thread.join()
        print(f"✅ Video saved: {video_filename}")
        send_to_backend(video_filename, "video")  # Send video to backend

# Start video and audio recording in a separate thread
video_thread = threading.Thread(target=record_continuous)
video_thread.start()

video_thread.join()

cap.release()
cv2.destroyAllWindows()

print("✅ Recording complete. Videos and audio saved successfully.")
