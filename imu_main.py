from src.imu import calibrate_offsets
from src.imu import process_imu_file
from src.imu import plot_raw_vs_filtered, plot_compare_imu_scaled
from src.imu import process_imu_offline
from src.imu import synchronize_imu_video
from src.imu import compute_knee_angle
from src.imu import debug_axes
from src.imu import plot_sync_analysis, plot_video_vs_imu_no_shift

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

calibrate_offsets("data/result_imu/raw/imu_session_live_1.csv", 3.0)

process_imu_file("data/result_imu/raw/imu_session_live_1.csv")

raw_csv = "data/result_imu/raw/imu_session_live_1.csv"
filtered_csv = "data/result_imu/filtered/live_1_filtered.csv"
features_csv = "data/result_imu/features/live_1_features.csv"

df_raw = pd.read_csv(raw_csv)
df_filt = pd.read_csv(filtered_csv)

plot_raw_vs_filtered(df_raw, df_filt, imu="imu0")
plot_raw_vs_filtered(df_raw, df_filt, imu="imu1")

plot_compare_imu_scaled(df_raw, df_filt)

# wczytaj przefiltrowane dane
df_filt = pd.read_csv(filtered_csv)

# debug osi
debug_axes(df_filt)

# oblicz kąty
knee_angle, thigh_pitch, shank_pitch = compute_knee_angle(df_filt)

print("THIGH min/max:", thigh_pitch.min(), thigh_pitch.max())
print("SHANK min/max:", shank_pitch.min(), shank_pitch.max())
print("KNEE min/max:", knee_angle.min(), knee_angle.max())

# --------------------------------------------------
# PLOT + SAVE ANGLES
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(df_filt["ts"], thigh_pitch, label="Thigh (IMU0)")
plt.plot(df_filt["ts"], shank_pitch, label="Shank (IMU1)")
plt.plot(df_filt["ts"], knee_angle, label="Knee Angle", linewidth=2)

plt.xlabel("Time (ms)")
plt.ylabel("Angle (deg)")
plt.title("Segment Angles + Knee Angle (IMU)")
plt.legend()
plt.grid(True)

# zapisz
Path("plots").mkdir(parents=True, exist_ok=True)
angle_plot_path = "plots/knee_angle.png"
plt.savefig(angle_plot_path, dpi=300)
print(f"Saved plot: {angle_plot_path}")

# Synchronizacja czasowa

process_imu_offline(
    "data/result_imu/filtered/live_1_filtered.csv",
    "data/result_imu/features/imu_session_live_1_features_time.csv"
)

synchronize_imu_video(
    video_csv="data/results/squat_analysis_1_frames.csv",
    imu_csv="data/result_imu/features/imu_session_live_1_features_time.csv",
    output_csv="data/result_all/imu_session_live_synced.csv"
)

plot_sync_analysis(
    synced_csv="data/result_all/imu_session_live_synced.csv",
    output_path="plots/video_vs_imu_sync.png"
)

plot_video_vs_imu_no_shift(
    video_csv="data/results/squat_analysis_1_frames.csv",  
    imu_csv="data/result_imu/features/imu_session_live_1_features_time.csv",
    output_path="plots/video_vs_imu_no_shift.png"
)