import pandas as pd
import os

def save_angles_csv(times, angles, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    df = pd.DataFrame({
        "time": times,
        "knee_raw": angles["knee"]["raw"],
        "knee_smooth": angles["knee"]["smooth"],
        "hip_raw": angles["hip"]["raw"],
        "hip_smooth": angles["hip"]["smooth"],
        "trunk_raw": angles["trunk"]["raw"],
        "trunk_smooth": angles["trunk"]["smooth"],
    })

    df.to_csv(path, index=False)

def save_squat_frames_csv(squats, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rows = []

    for squat in squats:
        for frame in squat["frames"]:
            rows.append({
                "time": frame["time"],
                "squat_id": frame["squat_id"],
                "phase": frame["phase"],
                "phase_percent": frame.get("phase_percent"),
                "knee": frame["knee"],
                "trunk": frame["trunk"],
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return df