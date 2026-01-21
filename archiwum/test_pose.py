import cv2
import mediapipe as mp
# import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision #zadania wizji komputerowej
from mediapipe.tasks.python.vision import RunningMode


#ścieżka do podstawowej konfiguracji 
base_options = python.BaseOptions(
    model_asset_path="pose_landmarker_lite.task"
)

#Konfiguracja PoseLandmarker
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=RunningMode.IMAGE,
    num_poses=1
)

# "kości"
POSE_CONNECTIONS = [
    (11, 13), (13, 15),   # lewa ręka
    (12, 14), (14, 16),   # prawa ręka
    (11, 12),             # barki
    (23, 25), (25, 27),   # lewa noga
    (24, 26), (26, 28),   # prawa noga
    (23, 24),             # biodra
]


pose_landmarker = vision.PoseLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0) # Użycie kamery internetowej

frame_counter = 0
try:
    while True:
        frame_counter += 1
        success, frame = cap.read() # Odczyt klatki z kamery
        if not success:
            break

        if frame_counter % 2 != 0:
            cv2.imshow("Pose", frame)
            continue

        #konwersja do formatu MediaPipe Image, inaczej nie przyjmie
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data = frame
        )

        result = pose_landmarker.detect(mp_image)

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
            for landmark in result.pose_landmarks[0]:
                # mnożymy przez szerokość i wysokość obrazu
                # x, y to nowy obszar
                x = int(landmark.x * w)
                y = int(landmark.y * h)

                #rysujemy zielony punkty
                cv2.circle(frame, (x,y), 4, (0, 255, 0), -1)

            
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
