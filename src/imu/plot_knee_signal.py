import pandas as pd
import matplotlib.pyplot as plt


def plot_knee_signal(csv_path):

    df = pd.read_csv(csv_path)

    plt.figure(figsize=(12,6))

    plt.plot(
        df["time_s"],
        df["knee_angle_imu"],
        color="green",
        linewidth=2,
        label="Knee angle (IMU)"
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Knee angle (deg)")
    plt.title("IMU Knee Angle Signal")

    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == "__main__":

    plot_knee_signal(
        "data/result_imu/features/imu_session_live_1_features_time.csv"
    )