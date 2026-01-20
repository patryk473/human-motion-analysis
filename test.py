import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Inicjalizacja detektora rąk
BaseOptions = vision.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    num_hands=2
)

detector = HandLandmarker.create_from_options(options)

# Teraz możesz używać detector.detect(img)
