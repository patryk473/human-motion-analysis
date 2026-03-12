import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# --------------------------------------------------
# LOAD EXAMPLE DATA
# --------------------------------------------------

video_path = "example_data/video_frames_sample.csv"
imu_path = "example_data/imu_sample.csv"

print("Loading example datasets...")

video_df = pd.read_csv(video_path)
imu_df = pd.read_csv(imu_path)


# --------------------------------------------------
# VIDEO DEMO
# --------------------------------------------------

print("Generating video knee angle plot...")

plt.figure(figsize=(10,5))

plt.plot(video_df["time"], video_df["knee_angle"], label="Video knee angle")

plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.title("Knee Angle from Video Pose Estimation")
plt.legend()
plt.grid(True)

Path("plots").mkdir(exist_ok=True)

plt.savefig("plots/example_video_knee_angle.png", dpi=300)


# --------------------------------------------------
# IMU DEMO
# --------------------------------------------------

print("Generating IMU knee angle plot...")

plt.figure(figsize=(10,5))

plt.plot(imu_df["time_s"], imu_df["knee_angle_imu"], label="IMU knee angle")

plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.title("Knee Angle from IMU Sensors")
plt.legend()
plt.grid(True)

plt.savefig("plots/example_imu_knee_angle.png", dpi=300)


print("Demo completed.")
print("Plots saved to 'plots/' directory.")