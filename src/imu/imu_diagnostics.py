import os
from pathlib import Path
import matplotlib.pyplot as plt

def plot_compare_imu_scaled(df_raw, df_filt, save=True):

    fig, axes = plt.subplots(3, 4, figsize=(18, 10))
    fig.suptitle("IMU0 vs IMU1 — Raw vs Filtered (Same Scale)")

    acc_axes = ["ax", "ay", "az"]
    gyro_axes = ["gx", "gy", "gz"]

    # ===============================
    # WYLICZENIE WSPÓLNYCH LIMITÓW
    # ===============================

    acc_min = min(
        df_raw[[f"imu0_a{a}" for a in "xyz"]].min().min(),
        df_raw[[f"imu1_a{a}" for a in "xyz"]].min().min(),
        df_filt[[f"imu0_a{a}_f" for a in "xyz"]].min().min(),
        df_filt[[f"imu1_a{a}_f" for a in "xyz"]].min().min(),
    )

    acc_max = max(
        df_raw[[f"imu0_a{a}" for a in "xyz"]].max().max(),
        df_raw[[f"imu1_a{a}" for a in "xyz"]].max().max(),
        df_filt[[f"imu0_a{a}_f" for a in "xyz"]].max().max(),
        df_filt[[f"imu1_a{a}_f" for a in "xyz"]].max().max(),
    )

    gyro_min = min(
        df_raw[[f"imu0_g{a}" for a in "xyz"]].min().min(),
        df_raw[[f"imu1_g{a}" for a in "xyz"]].min().min(),
        df_filt[[f"imu0_g{a}_f" for a in "xyz"]].min().min(),
        df_filt[[f"imu1_g{a}_f" for a in "xyz"]].min().min(),
    )

    gyro_max = max(
        df_raw[[f"imu0_g{a}" for a in "xyz"]].max().max(),
        df_raw[[f"imu1_g{a}" for a in "xyz"]].max().max(),
        df_filt[[f"imu0_g{a}_f" for a in "xyz"]].max().max(),
        df_filt[[f"imu1_g{a}_f" for a in "xyz"]].max().max(),
    )

    time = df_raw["ts"]

    # ===============================
    # RYSOWANIE
    # ===============================

    for i, axis in enumerate(acc_axes):

        # IMU0 ACC
        axes[i, 0].plot(time, df_raw[f"imu0_{axis}"], alpha=0.4)
        axes[i, 0].plot(time, df_filt[f"imu0_{axis}_f"], linewidth=2)
        axes[i, 0].set_title(f"IMU0 A{axis[-1].upper()}")
        axes[i, 0].set_ylim(acc_min, acc_max)
        axes[i, 0].grid(True)

        # IMU1 ACC
        axes[i, 1].plot(time, df_raw[f"imu1_{axis}"], alpha=0.4)
        axes[i, 1].plot(time, df_filt[f"imu1_{axis}_f"], linewidth=2)
        axes[i, 1].set_title(f"IMU1 A{axis[-1].upper()}")
        axes[i, 1].set_ylim(acc_min, acc_max)
        axes[i, 1].grid(True)

    for i, axis in enumerate(gyro_axes):

        # IMU0 GYRO
        axes[i, 2].plot(time, df_raw[f"imu0_{axis}"], alpha=0.4)
        axes[i, 2].plot(time, df_filt[f"imu0_{axis}_f"], linewidth=2)
        axes[i, 2].set_title(f"IMU0 G{axis[-1].upper()}")
        axes[i, 2].set_ylim(gyro_min, gyro_max)
        axes[i, 2].grid(True)

        # IMU1 GYRO
        axes[i, 3].plot(time, df_raw[f"imu1_{axis}"], alpha=0.4)
        axes[i, 3].plot(time, df_filt[f"imu1_{axis}_f"], linewidth=2)
        axes[i, 3].set_title(f"IMU1 G{axis[-1].upper()}")
        axes[i, 3].set_ylim(gyro_min, gyro_max)
        axes[i, 3].grid(True)

    plt.tight_layout()

    if save:
        Path("plots").mkdir(parents=True, exist_ok=True)
        save_path = "plots/imu_compare_scaled.png"
        plt.savefig(save_path, dpi=300)
        print(f"Saved plot: {save_path}")

    plt.close()


def plot_raw_vs_filtered(df_raw, df_filt, imu="imu0", save=True):

    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle(f"{imu.upper()} Raw vs Filtered")

    axes[0, 0].plot(df_raw["ts"], df_raw[f"{imu}_ax"], label="raw")
    axes[0, 0].plot(df_filt["ts"], df_filt[f"{imu}_ax_f"], label="filtered")
    axes[0, 0].set_title("AX")
    axes[0, 0].legend()

    axes[1, 0].plot(df_raw["ts"], df_raw[f"{imu}_ay"], label="raw")
    axes[1, 0].plot(df_filt["ts"], df_filt[f"{imu}_ay_f"], label="filtered")
    axes[1, 0].set_title("AY")
    axes[1, 0].legend()

    axes[2, 0].plot(df_raw["ts"], df_raw[f"{imu}_az"], label="raw")
    axes[2, 0].plot(df_filt["ts"], df_filt[f"{imu}_az_f"], label="filtered")
    axes[2, 0].set_title("AZ")
    axes[2, 0].legend()

    axes[0, 1].plot(df_raw["ts"], df_raw[f"{imu}_gx"], label="raw")
    axes[0, 1].plot(df_filt["ts"], df_filt[f"{imu}_gx_f"], label="filtered")
    axes[0, 1].set_title("GX")
    axes[0, 1].legend()

    axes[1, 1].plot(df_raw["ts"], df_raw[f"{imu}_gy"], label="raw")
    axes[1, 1].plot(df_filt["ts"], df_filt[f"{imu}_gy_f"], label="filtered")
    axes[1, 1].set_title("GY")
    axes[1, 1].legend()

    axes[2, 1].plot(df_raw["ts"], df_raw[f"{imu}_gz"], label="raw")
    axes[2, 1].plot(df_filt["ts"], df_filt[f"{imu}_gz_f"], label="filtered")
    axes[2, 1].set_title("GZ")
    axes[2, 1].legend()

    plt.tight_layout()

    if save:
        Path("plots").mkdir(parents=True, exist_ok=True)
        save_path = f"plots/{imu}_raw_vs_filtered.png"
        plt.savefig(save_path, dpi=300)
        print(f"Saved plot: {save_path}")
