from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MODELS = ROOT / "models" / "mediapipe"
POSE_LITE = MODELS / "pose_landmarker_lite.task"