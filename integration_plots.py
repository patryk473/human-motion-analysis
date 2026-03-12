import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_video_imu_analysis(csv_path):

    df = pd.read_csv(csv_path)

    out_dir = Path("plots/video_imu")
    out_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # 1 knee angle comparison
    # -------------------------------------------------

    plt.figure(figsize=(12,6))

    plt.plot(df["time"], df["knee_video"], label="knee video")
    plt.plot(df["time"], df["knee_imu"], label="knee imu")

    plt.xlabel("time (s)")
    plt.ylabel("angle (deg)")
    plt.title("Knee Angle: Video vs IMU")

    plt.legend()
    plt.grid()

    plt.savefig(out_dir / "knee_video_vs_imu.png")
    plt.close()

    # -------------------------------------------------
    # 2 knee error
    # -------------------------------------------------

    plt.figure(figsize=(12,6))

    plt.plot(df["time"], df["knee_error"])

    plt.xlabel("time (s)")
    plt.ylabel("deg")
    plt.title("Knee Angle Error (Video - IMU)")

    plt.grid()

    plt.savefig(out_dir / "knee_error.png")
    plt.close()

    # -------------------------------------------------
    # 3 squat cycles overlay
    # -------------------------------------------------

    plt.figure(figsize=(12,6))

    for sid in df["squat_id"].dropna().unique():

        squat = df[df["squat_id"] == sid]

        plt.plot(
            squat["phase_percent"],
            squat["knee_video"],
            alpha=0.4
        )

    plt.xlabel("phase (%)")
    plt.ylabel("knee angle (deg)")
    plt.title("Knee Angle – Video (All Squats)")

    plt.grid()

    plt.savefig(out_dir / "video_cycles_overlay.png")
    plt.close()

    # -------------------------------------------------
    # 4 mean squat cycle
    # -------------------------------------------------

    bins = np.linspace(0,100,101)

    df["phase_bin"] = np.digitize(df["phase_percent"], bins)

    mean_cycle = df.groupby("phase_bin").mean(numeric_only=True)

    plt.figure(figsize=(12,6))

    plt.plot(mean_cycle["knee_video"], label="video mean")
    plt.plot(mean_cycle["knee_imu"], label="imu mean")

    plt.xlabel("phase (%)")
    plt.ylabel("knee angle (deg)")
    plt.title("Mean Squat Cycle")

    plt.legend()
    plt.grid()

    plt.savefig(out_dir / "mean_cycle_video_vs_imu.png")
    plt.close()

    # -------------------------------------------------
    # 5 trunk vs thigh
    # -------------------------------------------------

    plt.figure(figsize=(12,6))

    plt.plot(df["time"], df["trunk_video"], label="trunk video")
    plt.plot(df["time"], df["thigh_pitch"], label="thigh pitch")

    plt.xlabel("time (s)")
    plt.ylabel("deg")
    plt.title("Segment Orientation")

    plt.legend()
    plt.grid()

    plt.savefig(out_dir / "trunk_vs_thigh.png")
    plt.close()

    # -------------------------------------------------
    # 6 dynamics
    # -------------------------------------------------

    plt.figure(figsize=(12,6))

    plt.plot(df["time"], df["omega_imu"], label="omega")
    plt.plot(df["time"], df["jerk_imu"], label="jerk")

    plt.xlabel("time (s)")
    plt.ylabel("value")
    plt.title("IMU Dynamics")

    plt.legend()
    plt.grid()

    plt.savefig(out_dir / "imu_dynamics.png")
    plt.close()

    # -------------------------------------------------
    # 7 ROM per squat
    # -------------------------------------------------

    rom = df.groupby("squat_id").agg({
        "knee_video": lambda x: x.max() - x.min(),
        "knee_imu": lambda x: x.max() - x.min()
    })

    plt.figure(figsize=(8,6))

    plt.scatter(rom["knee_video"], rom["knee_imu"])

    plt.xlabel("ROM video")
    plt.ylabel("ROM imu")
    plt.title("ROM Comparison")

    plt.grid()

    plt.savefig(out_dir / "rom_comparison.png")
    plt.close()

    print("plots saved to:", out_dir)


if __name__ == "__main__":

    plot_video_imu_analysis(
        "data/result_all/video_imu_dataset.csv"
    )