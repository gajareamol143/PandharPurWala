import cv2
import mediapipe as mp
import numpy as np
import datetime

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)  # Point A
    b = np.array(b)  # Point B
    c = np.array(c)  # Point C
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360.0 - angle
    
    return angle

# Webcam feed
cap = cv2.VideoCapture(0)

# Mediapipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Recolor the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Detect pose
        results = pose.process(image)

        # Recolor the image back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            # Extract landmarks
            landmarks = results.pose_landmarks.landmark

            # Get coordinates of key points
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
 
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            # Calculate the angle
            angle = calculate_angle(shoulder, hip, knee)
            current_time = datetime.datetime.now().time()
            # Display the posture status
            if  174 < angle < 178:
                status = "Good Posture"
              
                color = (0, 255, 0)  # Green
            else:
                status = "Bad Posture"
               
                color = (0, 0, 255)  # Red

            # Overlay status and angle on the frame
              
              
            cv2.putText(image, f'Posture: {status}', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
            with open('Output.txt','a') as file:
                    formatted_datetime = datetime.datetime.now()
                    file.write(status+ " " + formatted_datetime.strftime("%Y-%m-%d %H:%M:%S") + '\n')
            cv2.putText(image, f'Angle: {int(angle)}', (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        except Exception as e:
            print(f"Error: {e}")

        # Draw pose landmarks on the frame
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the frame
        cv2.imshow('Posture Detection', image)

        # Exit on pressing 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()