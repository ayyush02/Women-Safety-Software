import speech_recognition as sr
import threading
import time
import sounddevice as sd
import numpy as np
import wave
import os
import cv2
import requests

# Backend URL
BACKEND_URL = "http://192.168.43.211:3001/send-email"

# Create directories if they don't exist
os.makedirs("Audio", exist_ok=True)
os.makedirs("Videos", exist_ok=True)
os.makedirs("Pictures", exist_ok=True)

# Parameters
duration = 10  # seconds
sample_rate = 44100
channels = 2

# Try opening the camera
def initialize_camera():
    global cap
    for i in range(3):  # Try camera indexes 0, 1, 2
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✅ Camera opened successfully on index {i}")
            return
    print("❌ No available camera found! Exiting...")
    exit(1)  # Stop execution if no camera is found

# Initialize the camera
initialize_camera()

# Function to capture an image
def capture_image(image_file):
    time.sleep(2)  # Allow camera to adjust
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(image_file, frame)
        print(f"📸 Image saved: {image_file}")
    else:
        print("⚠ Failed to capture image.")

# Function to send data to backend
def send_to_backend(image_file, audio_file, video_file):
    print("📡 Sending data to backend...")

    try:
        with open(image_file, 'rb') as image, open(audio_file, 'rb') as audio, open(video_file, 'rb') as video:
            files = {
                'image': image,
                'audio': audio,
                'video': video
            }
            data = {
                'code': 'Emergency',
                'subject': 'Emergency Alert',
                'recipients': 'rohitkamblein2020@gmail.com'
            }

            response = requests.post(BACKEND_URL, files=files, data=data)

            if response.status_code == 200:
                print("✅ Data successfully sent to backend!")
            else:
                print(f"⚠ Error sending data: {response.text}")

    except Exception as e:
        print(f"❌ Failed to send data: {e}")

# Function to record audio
def record_audio(audio_file):
    print(f"🎙 Recording audio: {audio_file}")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()

    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"✔ Audio saved: {audio_file}")

# Function to record video in VLC-compatible format
def record_video(video_file):
    time.sleep(2)  # Allow camera to adjust before recording
    fourcc = cv2.VideoWriter_fourcc(*'X264')  # Use H.264 codec
    out = cv2.VideoWriter(video_file, fourcc, 20, (640, 480))

    if not cap.isOpened():
        print("❌ Camera failed to open for video recording!")
        return

    start_time = time.time()
    print(f"📹 Recording video: {video_file}")

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame from camera.")
            break
        out.write(frame)
        cv2.imshow("Recording", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    print(f"✔ Video saved: {video_file}")

# Function to listen for emergency words
def voice_trigger():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Listening for emergency words... (say 'help me' or 'emergency')")

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                print("🔄 Waiting for voice command...")
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio).lower()
                print(f"🎙 Recognized: {command}")

                if "help me" in command or "emergency" in command:
                    print("🚨 Emergency detected! Starting recording...")

                    timestamp = int(time.time())
                    image_file = f"Pictures/emergency_{timestamp}.jpg"
                    audio_file = f"Audio/emergency_{timestamp}.wav"
                    video_file = f"Videos/video_{timestamp}.mp4"  # VLC-compatible format

                    capture_image(image_file)
                    audio_thread = threading.Thread(target=record_audio, args=(audio_file,))
                    video_thread = threading.Thread(target=record_video, args=(video_file,))

                    audio_thread.start()
                    video_thread.start()

                    audio_thread.join()
                    video_thread.join()

                    send_to_backend(image_file, audio_file, video_file)

            except sr.WaitTimeoutError:
                print("⏳ No voice detected, continuing to listen...")
            except sr.UnknownValueError:
                print("🤷 Couldn't understand, trying again...")
            except sr.RequestError:
                print("⚠ Error connecting to speech service!")

# Start listening in a separate thread
voice_thread = threading.Thread(target=voice_trigger)
voice_thread.start()

cap.release()
cv2.destroyAllWindows()
