import numpy as np

def complementary_filter(acc_angle, gyro, dt, alpha=0.98):
    """
    Complementary filter for 1D angle estimation.

    acc_angle : angle from accelerometer (deg)
    gyro      : angular velocity (deg/s)
    dt        : time step (s)
    """

    fused_angle = np.zeros_like(acc_angle)

    fused_angle[0] = acc_angle[0]

    for i in range(1, len(acc_angle)):
        fused_angle[i] = (
            alpha * (fused_angle[i-1] + gyro[i] * dt[i]) +
            (1 - alpha) * acc_angle[i]
        )

    return fused_angle


def compute_pitch(ax, ay, az):
    """
    Estimate pitch angle (deg) from accelerometer.
    Works best for sagittal-plane motion (squat).
    """
    pitch = np.arctan2(ax, np.sqrt(ay**2 + az**2))
    return np.degrees(pitch)


def compute_segment_angles(df):

    dt = df["dt"].values

    # --- ACC ANGLE ---
    thigh_acc = compute_pitch(
        df["imu0_ax_f"],
        df["imu0_ay_f"],
        df["imu0_az_f"]
    )

    shank_acc = compute_pitch(
        df["imu1_ax_f"],
        df["imu1_ay_f"],
        df["imu1_az_f"]
    )

    # --- GYRO (deg/s) ---
    # Zakładamy że ruch w płaszczyźnie sagittal → używamy osi Y
    thigh_gyro = df["imu0_gy_f"].values
    shank_gyro = df["imu1_gy_f"].values

    # --- FUSION ---
    thigh_fused = complementary_filter(thigh_acc, thigh_gyro, dt)
    shank_fused = complementary_filter(shank_acc, shank_gyro, dt)

    return thigh_fused, shank_fused



def compute_knee_angle(df, neutral_time=3.0):

    thigh_pitch, shank_pitch = compute_segment_angles(df)

    # oszacowanie liczby próbek neutralnych
    dt_mean = df["dt"].iloc[1:].mean()
    fs = 1.0 / dt_mean
    neutral_samples = int(neutral_time * fs)

    thigh_neutral = np.mean(thigh_pitch[:neutral_samples])
    shank_neutral = np.mean(shank_pitch[:neutral_samples])

    thigh_corr = thigh_pitch - thigh_neutral
    shank_corr = shank_pitch - shank_neutral

    knee_angle = shank_corr - thigh_corr
    knee_angle = np.abs(knee_angle)

    return knee_angle, thigh_corr, shank_corr

