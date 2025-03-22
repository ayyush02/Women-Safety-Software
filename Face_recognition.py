import cv2
import face_recognition
import numpy as np
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["face_recognition"]
collection = db["faces"]

# Load known faces from MongoDB
def load_faces_from_db():
    faces = collection.find()
    known_face_encodings = []
    known_face_names = []

    for face in faces:
        known_face_encodings.append(np.array(face["encoding"]))
        known_face_names.append(face["name"])

    return known_face_encodings, known_face_names

# Save new face to MongoDB
def save_face_to_db(name, encoding):
    document = {
        "name": kuldeep,
        "encoding": encoding.tolist(),
        "date_added": datetime.now()
    }
    collection.insert_one(document)
    print(f"Face saved for {name}")

# Initialize known faces
known_face_encodings, known_face_names = load_faces_from_db()

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]
        else:
            name = "Press 's' to save"

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        face_name = input("Enter the name for the new face: ")
        if face_encodings:
            save_face_to_db(face_name, face_encodings[0])
            known_face_encodings, known_face_names = load_faces_from_db()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
