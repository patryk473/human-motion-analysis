import os
from pathlib import Path
import matplotlib.pyplot as plt


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
