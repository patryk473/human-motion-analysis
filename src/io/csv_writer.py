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

def save_squat_frames_csv(all_frames, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.DataFrame(all_frames)

    # kolejność kolumn (czytelność + stabilność)
    columns_order = [
        "frame",
        "time",

        "squat_id",
        "state",
        "phase",
        "phase_percent",

        "knee_angle",
        "hip_angle",
        "trunk_angle",

        # IMU – zostawiamy miejsce
        "imu1_ax", "imu1_ay", "imu1_az",
        "imu1_gx", "imu1_gy", "imu1_gz",
        "imu2_ax", "imu2_ay", "imu2_az",
        "imu2_gx", "imu2_gy", "imu2_gz",
    ]

    # tylko kolumny, które faktycznie istnieją
    columns_order = [c for c in columns_order if c in df.columns]

    df = df[columns_order]
    df.to_csv(output_path, index=False)

    return df