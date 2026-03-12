import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# --------------------------------
# Load example dataset
# --------------------------------

data_path = "example_data/video_frames_sample.csv"

df = pd.read_csv(data_path)

print("Loaded example dataset:", data_path)
print(df.head())


# --------------------------------
# Plot knee angle
# --------------------------------

plt.figure(figsize=(10,5))

plt.plot(df["time"], df["knee_angle"], label="Knee angle")
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.title("Example Knee Angle (Video)")
plt.legend()
plt.grid(True)

Path("plots").mkdir(exist_ok=True)

plt.savefig("plots/example_knee_angle.png", dpi=300)

plt.show()

print("Example plot saved to plots/example_knee_angle.png")