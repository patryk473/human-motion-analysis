from src.imu import calibrate_offsets
from src.imu import process_imu_file
from src.imu import fix_csv_dt
from src.imu import plot_raw_vs_filtered

import pandas as pd
import matplotlib.pyplot as plt
from src.imu import compute_knee_angle

calibrate_offsets("data/result_imu/raw/imu_session_live.csv", 3.0)

process_imu_file("data/result_imu/raw/imu_session_live.csv")

raw_csv = "data/result_imu/raw/imu_session_live.csv"
filtered_csv = "data/result_imu/filtered/live_filtered.csv"
features_csv = "data/result_imu/features/live_features.csv"

df_raw = pd.read_csv(raw_csv)
df_filt = pd.read_csv(filtered_csv)

plot_raw_vs_filtered(df_raw, df_filt, imu="imu0")
plot_raw_vs_filtered(df_raw, df_filt, imu="imu1")


# wczytaj przefiltrowane dane
df_filt = pd.read_csv(filtered_csv)

# oblicz kąty
knee_angle, thigh_pitch, shank_pitch = compute_knee_angle(df_filt)

from pathlib import Path

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

