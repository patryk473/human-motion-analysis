import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_video_vs_imu_no_shift(video_csv, imu_csv, output_path):

    video = pd.read_csv(video_csv)
    imu = pd.read_csv(imu_csv)

    # Zakładamy że oba startują od 0 czasu
    v_time = video["time"].values
    i_time = imu["time_s"].values

    knee_video = video["knee_angle"].values
    knee_imu = imu["knee_angle_imu"].values

    plt.figure(figsize=(12, 6))

    plt.plot(v_time, knee_video, label="VIDEO knee", linewidth=2)
    plt.plot(i_time, knee_imu, label="IMU knee (raw time)", linewidth=2)

    plt.xlabel("Time [s]")
    plt.ylabel("Knee angle [deg]")
    plt.title("VIDEO vs IMU (No Sync)")
    plt.legend()
    plt.grid(True)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {output_path}")

    plt.close()

    print("\nIMU min/max:",
          knee_imu.min(),
          knee_imu.max())

    print("VIDEO min/max:",
          knee_video.min(),
          knee_video.max())


if __name__ == "__main__":

    plot_video_vs_imu_no_shift(
        video_csv="data/results/squat_analysis_1_frames.csv",
        imu_csv="data/result_imu/features/imu_session_live_1_features_time.csv",
        output_path="plots/video_vs_imu_no_shift.png"
    )


def plot_sync_analysis(synced_csv, output_path):

    df = pd.read_csv(synced_csv)

    time = df["time"].values
    knee_video = df["knee_angle"].values
    knee_imu = df["knee_angle_imu_sync"].values

    # -----------------------------------Q
    # TWORZENIE WYKRESU
    # -----------------------------------
    plt.figure(figsize=(12, 6))

    plt.plot(time, knee_video, label="VIDEO knee", linewidth=2)
    plt.plot(time, knee_imu, label="IMU knee (synced)", linewidth=2)

    plt.xlabel("Time [s]")
    plt.ylabel("Knee angle [deg]")
    plt.title("VIDEO vs IMU Knee Angle")
    plt.legend()
    plt.grid(True)

    # -----------------------------------
    # ZAPIS DO PLIKU
    # -----------------------------------
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"📁 Saved plot: {output_path}")

    plt.close()

    # -----------------------------------
    # ANALIZA MINIMUM
    # -----------------------------------
    v_min_idx = np.argmin(knee_video)
    i_min_idx = np.argmin(knee_imu)

    v_min_time = time[v_min_idx]
    i_min_time = time[i_min_idx]

    print("\n===== MINIMUM ANALYSIS =====")
    print(f"Video min angle: {knee_video[v_min_idx]:.2f} deg at {v_min_time:.3f} s")
    print(f"IMU min angle:   {knee_imu[i_min_idx]:.2f} deg at {i_min_time:.3f} s")
    print(f"Time difference: {i_min_time - v_min_time:.3f} s")

    # -----------------------------------
    # RMSE
    # -----------------------------------
    v_norm = (knee_video - np.mean(knee_video)) / np.std(knee_video)
    i_norm = (knee_imu - np.mean(knee_imu)) / np.std(knee_imu)

    rmse = np.sqrt(np.mean((v_norm - i_norm) ** 2))

    print("\n===== SHAPE SIMILARITY =====")
    print(f"Normalized RMSE: {rmse:.4f}")
    print("0.0–0.3  → bardzo dobre dopasowanie")
    print("0.3–0.6  → umiarkowane dopasowanie")
    print(">0.6     → synchronizacja błędna")


if __name__ == "__main__":

    plot_sync_analysis(
        synced_csv="data/result_all/squat_02_synced.csv",
        output_path="plots/video_vs_imu_sync.png"
    )
