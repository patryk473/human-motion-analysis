from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import RunningMode
from src.config.paths import POSE_LITE

def create_pose_landmarker():
    #ścieżka do podstawowej konfiguracji 
    base_options = python.BaseOptions(
    model_asset_path=str(POSE_LITE)
    )

    #Konfiguracja PoseLandmarker
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=RunningMode.VIDEO,
        num_poses = 1
    )

    return vision.PoseLandmarker.create_from_options(options)