from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pygame
import os
import time

# Function to set system volume to 100%
def set_max_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(1.0, None)  # 1.0 = 100%

# Set volume to max
set_max_volume()

# Initialize pygame mixer
pygame.mixer.init()

# Define the audio file
audio_file = "alert_messege.mp3"  # Ensure this file exists in the correct path

# Check if the file exists
if os.path.exists(audio_file):
    pygame.mixer.music.load(audio_file)
    
    # Set pygame's audio volume to max (optional)
    pygame.mixer.music.set_volume(1.0)  # 1.0 is the highest volume
    
    # Play the message
    pygame.mixer.music.play()
    
    # Keep the script running until the audio is played
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)  # Reduce CPU usage
else:
    print("Audio file not found. Please check the path.")
