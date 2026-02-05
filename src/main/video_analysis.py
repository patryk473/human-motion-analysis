import cv2
import mediapipe as mp
import numpy as np

from src.config import create_pose_landmarker
from src.pose import draw_points, draw_connections, knee_flexion_angle, torso_tilt_angle, hip_angle, SquatDetector, RealTimeFeedback
from src.io import MovingAverage, draw_angles, draw_reports

POSE_CONNECTIONS = {
    "left": [(23, 25), (25, 27), (11, 23)],
    "right": [(24, 26), (26, 28), (12, 24)]
}

def analyze_video(video_path, side="left", smooth_window=5, show_video=True):
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    realtime = RealTimeFeedback()
    detector = SquatDetector(fps)
    frame_squat_ids = []
    
    success, frame = cap.read()
    if not success:
        raise RuntimeError("Nie można odczytać wideo")
    
    h, w, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter("data/processed/output.mp4",fourcc, fps, (w, h))

    pose_landmarker = create_pose_landmarker()  
    filters = {
        "knee" : MovingAverage(window=smooth_window),
        "hip" : MovingAverage(window=smooth_window),
        "trunk" : MovingAverage(window=smooth_window),
    } 

    angles = {
        "knee": {"raw": [],"smooth": []},
        "hip": {"raw": [],"smooth": []},
        "trunk": {"raw": [],"smooth": []},
    }
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

            t = timestamp_ms / 1000.0
            times.append(t)

            angle_knee = knee_flexion_angle(landmarks, w, h, side=side)
            angle_knee_smoothed = filters["knee"].update(angle_knee)

            angles["knee"]["raw"].append(angle_knee)
            angles["knee"]["smooth"].append(angle_knee_smoothed)

            angle_hip = hip_angle(landmarks, w, h, side=side)
            angle_hip_smoothed = filters["hip"].update(angle_hip)
            
            angles["hip"]["raw"].append(angle_hip)
            angles["hip"]["smooth"].append(angle_hip_smoothed)

            angle_trunk = torso_tilt_angle(landmarks, w, h, side=side)
            angle_trunk_smoothed = filters["trunk"].update(angle_trunk)

            angles["trunk"]["raw"].append(angle_trunk)
            angles["trunk"]["smooth"].append(angle_trunk_smoothed)

            feedback_msgs = realtime.evaluate(
                angle_knee_smoothed,
                angle_trunk_smoothed,
                detector.state
            )

            detector.update(angle_knee_smoothed, angle_trunk_smoothed, t)
            if detector.current_squat:
                current_id = detector.current_squat["squat_id"]
            else:
                current_id = None

            frame_squat_ids.append(current_id)

            if show_video:
                draw_connections(frame, landmarks, POSE_CONNECTIONS[side], w, h)
                draw_points(frame, landmarks, [11, 23, 25, 27], w, h)
                draw_angles(frame, angles)
                draw_reports(frame, angles, feedback_msgs)
                cv2.imshow("Pose analysis", frame)
            
            writer.write(frame)

        if show_video:
            if cv2.waitKey(1) & 0xFF in [27, ord("q")]:
                break

    writer.release()
    cap.release()
    cv2.destroyAllWindows()

    detector.normalize_squat_time()
    squats = detector.get_squats()
    squat_times = detector.compute_times()
    return times, angles, squats, squat_times
