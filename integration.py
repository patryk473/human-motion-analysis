import pandas as pd
import numpy as np
from pathlib import Path
from src.io import plot_video_imu_analysis

def compute_imu_dynamics(df):
    """
    Liczy wielkości dynamiczne IMU
    """

    omega = np.sqrt(
        df["imu0_gx_f"]**2 +
        df["imu0_gy_f"]**2 +
        df["imu0_gz_f"]**2
    )

    acc = np.sqrt(
        df["imu0_ax_f"]**2 +
        df["imu0_ay_f"]**2 +
        df["imu0_az_f"]**2
    )

    jerk = np.gradient(acc, df["time_sync"])

    df["omega_imu"] = omega
    df["acc_imu"] = acc
    df["jerk_imu"] = jerk

    return df


def build_video_imu_dataset(video_csv, imu_csv, offset):

    video = pd.read_csv(video_csv)
    imu = pd.read_csv(imu_csv)

    # ------------------------------------------------
    # synchronizacja czasu
    # ------------------------------------------------

    imu["time_sync"] = imu["time_s"] + offset

    # ------------------------------------------------
    # dynamika IMU
    # ------------------------------------------------

    imu = compute_imu_dynamics(imu)

    # ------------------------------------------------
    # sortowanie
    # ------------------------------------------------

    video = video.sort_values("time")
    imu = imu.sort_values("time_sync")

    # ------------------------------------------------
    # dopasowanie IMU → video
    # ------------------------------------------------

    merged = pd.merge_asof(
        video,
        imu,
        left_on="time",
        right_on="time_sync",
        direction="nearest"
    )

    # ------------------------------------------------
    # rename kolumn
    # ------------------------------------------------

    merged = merged.rename(columns={
        "knee_angle": "knee_video",
        "knee_angle_imu": "knee_imu",
        "trunk_angle": "trunk_video",
        "phase_new": "phase",
        "phase_percent_new": "phase_percent"
    })

    # ------------------------------------------------
    # error IMU vs video
    # ------------------------------------------------

    merged["knee_error"] = merged["knee_video"] - merged["knee_imu"]

    # ------------------------------------------------
    # final columns
    # ------------------------------------------------

    final_cols = [
        "time",
        "squat_id",
        "phase",
        "phase_percent",

        "knee_video",
        "knee_imu",
        "knee_error",

        "trunk_video",
        "thigh_pitch",
        "shank_pitch",

        "omega_imu",
        "acc_imu",
        "jerk_imu"
    ]

    merged = merged[final_cols]

    return merged


if __name__ == "__main__":

    video_csv = "data/results/squat_analysis_1_frames_phases.csv"
    imu_csv = "data/result_imu/features/imu_session_live_1_squats.csv"

    # offset synchronizacji (sekundy)
    offset = 0.0

    dataset = build_video_imu_dataset(video_csv, imu_csv, offset)

    out_path = Path("data/result_all/video_imu_dataset.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    dataset.to_csv(out_path, index=False)

    print("Dataset saved:", out_path)