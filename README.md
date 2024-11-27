# Drowsiness Detection System

## Project Overview

The **Drowsiness Detection System** is a real-time facial landmark detection application that helps detect signs of drowsiness by analyzing eye movement. Using computer vision and machine learning techniques, the system calculates the Eye Aspect Ratio (EAR) to determine whether a person is drowsy based on their eye movements. If drowsiness is detected, the system triggers an alarm to alert the person. This project utilizes **Streamlit** for the web interface, **OpenCV** for video processing, and **MediaPipe** for facial landmark detection.

## Features

- Real-time drowsiness detection using webcam or uploaded video.
- Eye Aspect Ratio (EAR) calculation to monitor drowsiness.
- Visual feedback with facial landmarks drawn on the face.
- Alarm system that sounds when drowsiness is detected.
- User-friendly interface built with **Streamlit**.
- Option to upload a video or use the webcam for real-time detection.

## Demo

![Drowsiness Detection](https://github.com/mahmouddbelo/Drowsiness-Detection-System/blob/main/test%20-%20Google%20Chrome%2011_26_2024%206_41_02%20PM.png)  <!-- Replace with your image link -->

### How it Works

1. **Facial Landmark Detection**: The system uses **MediaPipe**'s Face Mesh model to detect key facial landmarks, specifically around the eyes.
2. **Eye Aspect Ratio Calculation**: The Eye Aspect Ratio (EAR) is calculated based on the distance between the eye landmarks. If the EAR falls below a certain threshold, it indicates drowsiness.
3. **Alarm Trigger**: If drowsiness is detected for a certain number of consecutive frames, an alarm sound is triggered.
4. **Real-Time Monitoring**: The system continuously monitors the user's eyes using either the webcam or a video file.

## Requirements
requirements.txt:
```bash
streamlit==1.19.0
opencv-python-headless==4.7.0.72
mediapipe==0.9.1
pygame==2.5.0
numpy==1.23.5
```
Libraries Used
Streamlit: For building the web application interface.
OpenCV: For processing video frames and detecting facial landmarks.
MediaPipe: For performing facial landmark detection.
Pygame: For playing the alarm sound.
NumPy: For numerical operations, specifically in calculating the Eye Aspect Ratio (EAR)

## Installation & Setup
### 1)Clone the Repository:
```bash
git clone https://github.com/mahmouddbelo/Drowsiness-Detection-System.git
cd Drowsiness-Detection-System
```
### 2)Install Dependencies: Ensure you have Python 3.7 or above installed. Then, install all the required dependencies:
```bash
pip install -r requirements.txt
```
### 3)Run the Application: To run the Drowsiness Detection System, use the following command:
```bash
streamlit run test.py
```
This will open a new tab in your browser where you can interact with the system.
## Usage
### Option 1: Use Webcam
Click on the "Start Webcam" button to start the webcam.
The system will begin processing the video feed in real-time.
If drowsiness is detected, an alarm will sound and a warning message will be displayed.
### Option 2: Upload Video
Choose a pre-recorded video file by uploading it.
The system will process the video file frame by frame for drowsiness detection.
## Replacing the Alarm Sound
By default, the system uses a built-in alarm sound from Pygame when drowsiness is detected. If you'd like to replace the alarm sound with your own preferred sound, follow these steps:
### 1)Find a sound file (e.g., .mp3 or .wav) that you would like to use for the alarm.
### 2)Place the sound file in the same directory as your project.
### 3)In the test.py file, locate the following lines of code:
```bash
pygame.mixer.init()
pygame.mixer.music.load('alarm_sound.mp3')  # Default alarm sound file
pygame.mixer.music.play(-1)  # Play sound indefinitely
```
### 4)Replace 'alarm_sound.mp3' with the filename of your preferred sound.
Example:
```bash
pygame.mixer.music.load('your_custom_sound.wav')  # Your custom sound
```
Now, when drowsiness is detected, the system will play your chosen alarm sound.
## Contributing
Feel free to fork this project, open issues, or submit pull requests. If you have suggestions for improvements or features, please open an issue, and I'll get back to you.
## Acknowledgements
### OpenCV for real-time video processing and facial landmark detection.
### MediaPipe for efficient face mesh and landmark detection.
#### Streamlit for creating the interactive web interface.
### Pygame for the alarm sound feature.
## The drowsiness detection concept inspired by several real-world applications in safety-critical environments such as driving.


