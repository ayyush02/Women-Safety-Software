import numpy as np
import librosa
import pyaudio
import wave
from sklearn.svm import SVC
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import soundfile as sf
import os
import warnings
warnings.filterwarnings("ignore")

# Record audio from microphone
def record_audio(output_file, duration=5, sr=16000):
    """Record audio from microphone and save to a WAV file."""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # Mono
    RATE = sr

    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)

        print(f"Recording for {duration} seconds...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return output_file
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None

# Audio preprocessing and feature extraction
def extract_mfcc_features(audio_path, sr=16000, n_mfcc=13):
    """Extract MFCC features from an audio file."""
    try:
        audio, sample_rate = librosa.load(audio_path, sr=sr)
        mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
        return np.mean(mfcc.T, axis=0)
    except Exception as e:
        print(f"Error extracting MFCC features from {audio_path}: {e}")
        return None

def segment_audio(audio_path, sr=16000, frame_duration=30, energy_threshold=0.01):
    """Segment audio into speech frames using energy-based VAD."""
    try:
        audio, sr = sf.read(audio_path)
        frame_len = int(sr * frame_duration / 1000)  # Frame length in samples

        segments = []
        for i in range(0, len(audio) - frame_len, frame_len):
            frame = audio[i:i + frame_len]
            energy = np.sum(frame ** 2) / len(frame)
            if energy > energy_threshold:
                mfcc = librosa.feature.mfcc(y=frame, sr=sr, n_mfcc=13)
                segments.append(np.mean(mfcc.T, axis=0))
        return np.array(segments)
    except Exception as e:
        print(f"Error segmenting audio {audio_path}: {e}")
        return np.array([])

# Speaker Identification
def train_speaker_id_model(audio_files, labels):
    """Train an SVM model for speaker identification."""
    X = []
    for file in audio_files:
        if not os.path.exists(file):
            print(f"Audio file not found: {file}")
            return None, None
        features = extract_mfcc_features(file)
        if features is None:
            return None, None
        X.append(features)
    
    y = labels
    try:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = SVC(kernel='linear', probability=True)
        model.fit(X_scaled, y)
        return model, scaler
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None

def identify_speaker(model, scaler, audio_path):
    """Identify the speaker in a given audio file."""
    if model is None or scaler is None:
        print("Model or scaler not initialized.")
        return None, None
    features = extract_mfcc_features(audio_path)
    if features is None:
        return None, None
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)[0]
    confidence = model.predict_proba(features_scaled)[0].max()
    return prediction, confidence

# Speaker Diarization
def diarize_speakers(audio_path, num_speakers=None):
    """Perform speaker diarization using clustering."""
    segments = segment_audio(audio_path)
    if len(segments) == 0:
        return "No speech detected"

    try:
        scaler = StandardScaler()
        segments_scaled = scaler.fit_transform(segments)
        clustering = AgglomerativeClustering(n_clusters=num_speakers, linkage='ward')
        labels = clustering.fit_predict(segments_scaled)

        diarization_result = []
        for i, label in enumerate(labels):
            start_time = i * 0.03  # 30ms frames
            end_time = (i + 1) * 0.03
            diarization_result.append((start_time, end_time, f"Speaker_{label}"))
        return diarization_result
    except Exception as e:
        print(f"Error in diarization: {e}")
        return "Diarization failed"

# Main execution
def main():
    # Record training data
    print("Please record audio for Speaker 1:")
    speaker1_file = record_audio("speaker1.wav", duration=5)
    if speaker1_file is None:
        return

    print("Please record audio for Speaker 2:")
    speaker2_file = record_audio("speaker2.wav", duration=5)
    if speaker2_file is None:
        return

    train_files = [speaker1_file, speaker2_file]
    train_labels = [0, 1]  # Speaker IDs (0 for speaker1, 1 for speaker2)

    # Record test audio
    print("Please record test audio:")
    test_file = record_audio("recorded_test.wav", duration=5)
    if test_file is None:
        return

    # Train speaker identification model
    print("Training speaker identification model...")
    model, scaler = train_speaker_id_model(train_files, train_labels)
    if model is None or scaler is None:
        return

    # Identify speaker in recorded audio
    print("\nSpeaker Identification (on recorded audio):")
    speaker_id, confidence = identify_speaker(model, scaler, test_file)
    if speaker_id is not None and confidence is not None:
        print(f"Predicted Speaker ID: {speaker_id}, Confidence: {confidence:.2f}")

    # Perform speaker diarization on recorded audio
    print("\nSpeaker Diarization (on recorded audio):")
    diarization = diarize_speakers(test_file)
    if isinstance(diarization, str):
        print(diarization)
    else:
        for start, end, speaker in diarization:
            print(f"{speaker} from {start:.2f}s to {end:.2f}s")

if __name__ == "__main__":
    # Install dependencies if not already installed:
    # pip install numpy librosa scikit-learn soundfile pyaudio
    main()