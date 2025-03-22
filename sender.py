import cv2
import sounddevice as sd
import numpy as np
import wave
import time
import os
import threading
import requests
import speech_recognition as sr
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pygame

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

# Function to play alert audio immediately after script starts
def play_alert_audio():
    print("🔊 Playing alert audio (Only Once at Start)")

    # Set system volume to max
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(1.0, None)  # 1.0 = 100%

    # Initialize pygame mixer
    pygame.mixer.init()

    # Define the audio file
    audio_file = "alert_messege.mp3"  # Ensure this file exists in the correct path

    # Check if the file exists
    if os.path.exists(audio_file):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.set_volume(1.0)  # Set pygame volume to max
        pygame.mixer.music.play()
        
        # Keep the script running until the audio is played
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)  # Reduce CPU usage
    else:
        print("❌ Audio file not found. Please check the path.")

# Function to send file to backend
def send_to_backend(file_path, file_type):
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempting to upload {file_type}: {file_path} to {BACKEND_URL} (Attempt {attempt + 1}/{max_retries})")
            with open(file_path, "rb") as f:
                files = {file_type: (file_path, f)}
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
        video_filename = f"Videos/video_{timestamp}.avi"
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

# Function to listen for voice command to start recording
def voice_activation():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Listening for 'start recording' command...")

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                print("🔄 Waiting for voice command...")
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio).lower()
                print(f"🎙 Recognized: {command}")

                if "start recording" in command:
                    print("🚨 Voice command detected! Starting recording...")
                    return  # Exit function and start recording

            except sr.WaitTimeoutError:
                print("⏳ No voice detected, continuing to listen...")
            except sr.UnknownValueError:
                print("🤷 Couldn't understand, trying again...")

# Initialize camera
initialize_camera()

# Play alert message immediately at script start
play_alert_audio()

# Wait for voice activation before starting
voice_activation()

# Start video and audio recording in a separate thread
video_thread = threading.Thread(target=record_continuous)
video_thread.start()

video_thread.join()

cap.release()
cv2.destroyAllWindows()

print("✅ Recording complete. Videos and audio saved successfully.")
