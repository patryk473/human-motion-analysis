import cv2
import mediapipe as mp
import numpy as np

from src.config import create_pose_landmarker
from src.pose import draw_points, draw_connections, knee_flexion_angle
from src.io import MovingAverage

POSE_CONNECTIONS = [
    (23, 25), (25, 27),   # lewa noga
]

def analyze_video(video_path, side="left", smooth_window=5, show_video=True):
    
    cap = cv2.VideoCapture("data/raw/knee_flexion_01.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)

    pose_landmarker = create_pose_landmarker()  
    ma_filter = MovingAverage(window=smooth_window)

    angles_raw = []
    angles_smooth = []
    times = []

    frame_counter = 0

    while True:
        frame_counter += 1
        success, frame = cap.read() # Odczyt klatki z kamery
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        timestamp_ms = int(frame_counter * 1000 / fps)

        #konwersja do formatu MediaPipe Image, inaczej nie przyjmie
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data = rgb
        )

        result = pose_landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.pose_landmarks: 
            h, w, _ = frame.shape
            landmarks = result.pose_landmarks[0]

            angle = knee_flexion_angle(landmarks, w, h, side=side)
            angle_smoothed = ma_filter.update(angle)

            t = frame_counter / fps
            times.append(t)
            angles_raw.append(angle)
            angles_smooth.append(angle_smoothed)
            
            if show_video:
                draw_connections(frame, landmarks, POSE_CONNECTIONS, w, h)
                draw_points(frame, landmarks, [23, 25, 27], w, h)
                
                cv2.putText(
                    frame,
                    f"{angle_smoothed:.1f}",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )

                cv2.imshow("Pose analysis", frame)

        if show_video:
            if cv2.waitKey(1) & 0xFF in [27, ord("q")]:
                break


    cap.release()
    cv2.destroyAllWindows()

    return times, angles_raw, angles_smooth
