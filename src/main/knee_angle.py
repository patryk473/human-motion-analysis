import cv2
import mediapipe as mp
import numpy as np
# import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision #zadania wizji komputerowej
from mediapipe.tasks.python.vision import RunningMode

from src.pose import angle_3_points
from src.config import create_pose_landmarker

pose_landmarker = create_pose_landmarker()

# "kości"
POSE_CONNECTIONS = [
    (23, 25), (25, 27),   # lewa noga
    # (24, 26), (26, 28),   # prawa noga
    # (23, 24),             # biodra
]

cap = cv2.VideoCapture("data/raw/knee_flexion_01.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)

frame_counter = 0
try:
    while True:
        frame_counter += 1
        success, frame = cap.read() # Odczyt klatki z kamery
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        timestamp_ms = int(frame_counter * 1000 / fps)

        if frame_counter % 2 != 0:
            cv2.imshow("Pose", frame)
            cv2.waitKey(1)
            continue

        #konwersja do formatu MediaPipe Image, inaczej nie przyjmie
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data = rgb
        )

        result = pose_landmarker.detect_for_video(mp_image, timestamp_ms)


        if result.pose_landmarks: 
            # rysowanie punktów
            h, w, _ = frame.shape

            for start_idx, end_idx in POSE_CONNECTIONS:
                p1 = result.pose_landmarks[0][start_idx]
                p2 = result.pose_landmarks[0][end_idx]

                x1, y1 = int(p1.x * w), int(p1.y * h)
                x2, y2 = int(p2.x * w), int(p2.y * h)

                cv2.line(frame, (x1,y1), (x2,y2), (255, 0, 0), 2)

            # result.pose_landmark to:
            # lista POZ (osób) -> każda pozycja = lista punktów ciała
            # Iteracja po 33 punktach osoby
            # result.pose_landmarks[0][i] <- i-ty punkt osoby
            for idx in [23, 25, 27, 29, 31]:
                # mnożymy przez szerokość i wysokość obrazu
                # x, y to nowy obszar
                landmark = result.pose_landmarks[0][idx]
                x = int(landmark.x * w)
                y = int(landmark.y * h)

                #rysujemy zielony punkty
                cv2.circle(frame, (x,y), 4, (0, 255, 0), -1)

            biodro = result.pose_landmarks[0][23]
            kolano = result.pose_landmarks[0][25]
            kostka = result.pose_landmarks[0][27]

            A = np.array([biodro.x * w, biodro.y * h])
            B = np.array([kolano.x * w, kolano.y * h])
            C = np.array([kostka.x * w, kostka.y * h])

            angle = angle_3_points(A,B,C) #w stopniach

            cv2.putText(
                frame,
                f"{angle:.1f}",
                (int(B[0] +10), int(B[1])),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            cv2.imshow("Pose", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

finally:
    print("Zamykanie programu...")
    cap.release()
    cv2.destroyAllWindows()
    for _ in range(5):
        cv2.waitKey(1)
