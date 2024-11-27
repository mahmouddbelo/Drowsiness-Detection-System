import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time
from pathlib import Path
import tempfile
import threading
import base64
import os
from pygame import mixer
import io

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Constants for eye aspect ratio calculation
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 20

# Initialize counters
COUNTER = 0
ALARM_ON = False

# Define eye landmarks indices for MediaPipe
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Encoded MP3 alarm sound (base64 string of a simple beep sound)
mp3_file_path = r"C:\Users\MBR\Downloads\drowsness\zapsplat_sport_air_horn_2x_blasts_001_21150.mp3"

# Read the MP3 file and encode it to Base64
with open(mp3_file_path, "rb") as mp3_file:
    encoded_mp3 = base64.b64encode(mp3_file.read()).decode("utf-8")

# Replace the ALARM_SOUND_BASE64 variable
ALARM_SOUND_BASE64 = f"""
{encoded_mp3}
"""

def initialize_sound():
    """Initialize pygame mixer and load the alarm sound"""
    try:
        mixer.init()
        # Decode base64 sound and save it temporarily
        sound_data = base64.b64decode(ALARM_SOUND_BASE64)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(sound_data)
            return temp_file.name
    except Exception as e:
        st.error(f"Error initializing sound: {str(e)}")
        return None

def play_alarm_sound(sound_path):
    """Play alarm sound using pygame mixer"""
    try:
        if not mixer.get_busy():  # Only play if not already playing
            sound = mixer.Sound(sound_path)
            sound.play()
    except Exception as e:
        st.error(f"Error playing sound: {str(e)}")

def calculate_ear(landmarks, eye_indices):
    """Calculate eye aspect ratio for given eye indices"""
    try:
        points = []
        for index in eye_indices:
            point = landmarks[index]
            points.append([point.x, point.y])
        
        points = np.array(points)
        vertical_dist1 = np.linalg.norm(points[1] - points[5])
        vertical_dist2 = np.linalg.norm(points[2] - points[4])
        horizontal_dist = np.linalg.norm(points[0] - points[3])
        
        ear = (vertical_dist1 + vertical_dist2) / (2.0 * horizontal_dist)
        return ear
    except:
        return 0.0

def draw_landmarks(frame, landmarks, frame_width, frame_height):
    """Draw landmarks and connections on the frame"""
    for landmark in landmarks.landmark:
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
    
    for eye in [LEFT_EYE, RIGHT_EYE]:
        points = []
        for index in eye:
            point = landmarks.landmark[index]
            x = int(point.x * frame_width)
            y = int(point.y * frame_height)
            points.append([x, y])
        
        points = np.array(points, dtype=np.int32)
        cv2.polylines(frame, [points], True, (0, 255, 0), 1)

def process_frame(frame, sound_path):
    """Process each frame for drowsiness detection"""
    global COUNTER, ALARM_ON
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_height, frame_width = frame.shape[:2]
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            draw_landmarks(frame, face_landmarks, frame_width, frame_height)
            
            left_ear = calculate_ear(face_landmarks.landmark, LEFT_EYE)
            right_ear = calculate_ear(face_landmarks.landmark, RIGHT_EYE)
            ear = (left_ear + right_ear) / 2.0
            
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if not ALARM_ON:
                        ALARM_ON = True
                        st.warning("⚠️ DROWSINESS ALERT! Wake up!", icon="⚠️")
                        # Play alarm sound in a separate thread
                        threading.Thread(target=play_alarm_sound, args=(sound_path,), daemon=True).start()
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                COUNTER = 0
                ALARM_ON = False
            
            cv2.putText(frame, f"EAR: {ear:.2f}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    else:
        cv2.putText(frame, "No face detected", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    return frame

def process_webcam(sound_path):
    """Handle webcam input"""
    st.write("Webcam activated. Press 'Stop' to end the session.")
    
    video_placeholder = st.empty()
    stop_button = st.button('Stop')
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    try:
        while not stop_button:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access webcam")
                break
            
            frame = cv2.flip(frame, 1)
            processed_frame = process_frame(frame, sound_path)
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(rgb_frame, channels="RGB", use_column_width=True)
            time.sleep(0.01)
            
            if stop_button:
                break
                
    finally:
        cap.release()

def process_video_file(video_file, sound_path):
    """Handle video file input"""
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    
    st.write("Video uploaded successfully. Processing...")
    video_placeholder = st.empty()
    stop_button = st.button('Stop Processing')
    
    cap = cv2.VideoCapture(tfile.name)
    
    try:
        while cap.isOpened() and not stop_button:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = process_frame(frame, sound_path)
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(rgb_frame, channels="RGB", use_column_width=True)
            time.sleep(0.01)
            
    finally:
        cap.release()
        Path(tfile.name).unlink()

def main():
    st.title("Drowsiness Detection System")
    
    # Initialize sound
    sound_path = initialize_sound()
    
    # Add custom CSS for better styling
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            height: 3em;
            margin: 1em 0;
        }
        .upload-text {
            text-align: center;
            padding: 2em;
            border: 2px dashed #ccc;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.write("""
    Welcome to the Drowsiness Detection System! This application can help detect signs of drowsiness 
    using either your webcam or a pre-recorded video. Choose your preferred input method below.
    """)
    
    # Create two columns for the input options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Option 1: Use Webcam")
        if st.button("Start Webcam"):
            process_webcam(sound_path)
    
    with col2:
        st.subheader("Option 2: Upload Video")
        video_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov'])
        if video_file is not None:
            process_video_file(video_file, sound_path)
    
    # Add information about the system
    st.markdown("---")
    st.markdown("""
    ### How it works:
    1. The system tracks your facial landmarks in real-time
    2. It monitors your eye movements and calculates the Eye Aspect Ratio (EAR)
    3. If your eyes remain closed for too long, an alert will be triggered with sound
    
    ### Tips for best results:
    - Ensure good lighting in your environment
    - Position your face clearly in front of the camera
    - Maintain a reasonable distance from the camera
    - Try to keep your head relatively still
    """)

    # Cleanup
    if sound_path and os.path.exists(sound_path):
        try:
            os.unlink(sound_path)
        except:
            pass

if __name__ == "__main__":
    main()