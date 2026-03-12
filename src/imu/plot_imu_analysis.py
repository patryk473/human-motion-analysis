import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_for_imu_analysis(csv_path):

    df = pd.read_csv(csv_path)

    out_dir = Path("plots")
    out_dir.mkdir(exist_ok=True)

    # ----------------------------
    # knee angle
    # ----------------------------

    plt.figure(figsize=(12,6))

    plt.plot(df["time_s"], df["knee_angle_imu"], label="knee angle")

    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.title("IMU Knee Angle")

    plt.grid()
    plt.legend()

    plt.savefig(out_dir / "imu_knee_angle.png")
    plt.close()


    # ----------------------------
    # segment orientation
    # ----------------------------

    plt.figure(figsize=(12,6))

    plt.plot(df["time_s"], df["thigh_pitch"], label="thigh pitch")
    plt.plot(df["time_s"], df["shank_pitch"], label="shank pitch")

    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.title("Segment Orientation")

    plt.grid()
    plt.legend()

    plt.savefig(out_dir / "imu_segment_angles.png")
    plt.close()


    # ----------------------------
    # gyro magnitude
    # ----------------------------

    gyro = np.sqrt(
        df["imu0_gx_f"]**2 +
        df["imu0_gy_f"]**2 +
        df["imu0_gz_f"]**2
    )

    plt.figure(figsize=(12,6))

    plt.plot(df["time_s"], gyro, label="gyro magnitude")

    plt.xlabel("Time (s)")
    plt.ylabel("rad/s")
    plt.title("Angular Velocity")

    plt.grid()
    plt.legend()

    plt.savefig(out_dir / "imu_gyro_magnitude.png")
    plt.close()


    # ----------------------------
    # acceleration magnitude
    # ----------------------------

    acc = np.sqrt(
        df["imu0_ax_f"]**2 +
        df["imu0_ay_f"]**2 +
        df["imu0_az_f"]**2
    )

    plt.figure(figsize=(12,6))

    plt.plot(df["time_s"], acc, label="acc magnitude")

    plt.xlabel("Time (s)")
    plt.ylabel("m/s²")
    plt.title("Acceleration Magnitude")

    plt.grid()
    plt.legend()

    plt.savefig(out_dir / "imu_acc_magnitude.png")
    plt.close()

    print("IMU plots saved in /plots")