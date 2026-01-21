#nie działa zamykanie poza tym mega spoko

import cv2
import mediapipe as mp
# import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision #zadania wizji komputerowej
from mediapipe.tasks.python.vision import RunningMode


#ścieżka do podstawowej konfiguracji 
base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

#Konfiguracja HandLandmarker
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=RunningMode.IMAGE,
    num_hands=1
)

#odpowiednim starego hands = mp.solutions.hands.Hands() / utworzenie detektora dłoni
hand_landmarker = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0) # Użycie kamery internetowej

frame_counter = 0
try:
    while True:
        frame_counter += 1
        success, frame = cap.read() # Odczyt klatki z kamery
        if not success:
            break

        if frame_counter % 2 != 0:
            cv2.imshow("Hand", frame)
            continue

        #konwersja do formatu MediaPipe Image, inaczej nie przyjmie
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data = frame
        )

        #nowa detekcja dłoni
        # w tym momencie result zawiera result.hand_landmarks
        # listę dłoni <- każda dłoń 21 punktów
        result = hand_landmarker.detect(mp_image)

        if result.hand_landmarks: # sprawdzenie czy wykryto dłoń
            for hand_landmarks in result.hand_landmarks:
                # rysowanie punktów
                h, w, _ = frame.shape

                for landmark in hand_landmarks:
                    # mnożymy przez szerokość i wysokość obrazu
                    # x, y to nowy obszar
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)

                    #rysujemy zielony punkty
                    cv2.circle(frame, (x,y), 5, (0, 255, 0), -1)

                # timestamp_ms = int(time.time() * 1000)
                # result = hand_landmarker.detect_for_video(mp_image, timestamp_ms)

                cv2.imshow("Hand", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:
                    break

finally:
    print("Zamykanie programu...")
    cap.release()
    cv2.destroyAllWindows()
    for _ in range(5):
        cv2.waitKey(1)
