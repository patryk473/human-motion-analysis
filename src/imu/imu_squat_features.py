import numpy as np
import pandas as pd


def compute_imu_squat_features(df):
    """
    Liczy cechy IMU dla każdego przysiadu.

    Wymaga kolumn:
        imu_squat_id
        imu_phase
        knee_angle_imu
        imu*_ax_f
        imu*_ay_f
        imu*_az_f
        imu*_gx_f
        imu*_gy_f
        imu*_gz_f
    """

    results = []

    for squat_id in df["imu_squat_id"].dropna().unique():

        squat = df[df["imu_squat_id"] == squat_id]

        # ------------------------------
        # ROM kolana
        # ------------------------------

        knee_rom = squat["knee_angle_imu"].max() - squat["knee_angle_imu"].min()

        # ------------------------------
        # ACC norm
        # ------------------------------

        acc = np.sqrt(
            squat["imu0_ax_f"]**2 +
            squat["imu0_ay_f"]**2 +
            squat["imu0_az_f"]**2
        )

        acc_rms = np.sqrt(np.mean(acc**2))
        acc_var = np.var(acc)

        # ------------------------------
        # GYRO norm
        # ------------------------------

        gyro = np.sqrt(
            squat["imu0_gx_f"]**2 +
            squat["imu0_gy_f"]**2 +
            squat["imu0_gz_f"]**2
        )

        gyro_rms = np.sqrt(np.mean(gyro**2))
        gyro_var = np.var(gyro)
        gyro_peak = np.max(np.abs(gyro))

        # ------------------------------
        # JERK (płynność ruchu)
        # ------------------------------

        jerk = np.diff(acc)
        jerk_rms = np.sqrt(np.mean(jerk**2))

        # ------------------------------
        # CZASY FAZ
        # ------------------------------

        descent = squat[squat["imu_phase"] == "descent"]
        ascent = squat[squat["imu_phase"] == "ascent"]

        descent_time = (
            descent["time_s"].iloc[-1] - descent["time_s"].iloc[0]
            if len(descent) > 1 else np.nan
        )

        ascent_time = (
            ascent["time_s"].iloc[-1] - ascent["time_s"].iloc[0]
            if len(ascent) > 1 else np.nan
        )

        results.append({

            "imu_squat_id": squat_id,

            "knee_rom": knee_rom,

            "acc_rms": acc_rms,
            "acc_var": acc_var,

            "gyro_rms": gyro_rms,
            "gyro_var": gyro_var,
            "gyro_peak": gyro_peak,

            "jerk_rms": jerk_rms,

            "descent_time": descent_time,
            "ascent_time": ascent_time
        })

    return pd.DataFrame(results)