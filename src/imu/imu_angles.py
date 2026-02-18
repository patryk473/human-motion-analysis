import numpy as np


# ==========================================================
# COMPLEMENTARY FILTER
# ==========================================================

def complementary_filter(acc_angle, gyro_rate, dt, alpha=0.98):

    fused = np.zeros_like(acc_angle)
    fused[0] = acc_angle[0]

    for i in range(1, len(acc_angle)):

        predicted = fused[i-1] + gyro_rate[i] * dt[i]

        error = acc_angle[i] - predicted
        error = (error + 180) % 360 - 180

        fused[i] = predicted + (1 - alpha) * error

    return fused



# ==========================================================
# PITCH FROM ACCELEROMETER (SPÓJNA DEFINICJA)
# ==========================================================

def compute_pitch(ax, ay, az):
    """
    Pitch angle relative to gravity (deg).
    Assumes sagittal plane motion.
    """
    pitch = np.arctan2(ax, np.sqrt(ay**2 + az**2))
    return np.degrees(pitch)


def compute_segment_orientation(ax, ay, az, gyro_axis, dt, imu_name):

    if imu_name == "imu0":
        acc_angle = np.degrees(np.arctan2(ax, -ay))

    elif imu_name == "imu1":
        acc_angle = np.degrees(np.arctan2(az, -ay))  # TEST

    fused = complementary_filter(acc_angle, gyro_axis, dt)

    fused = np.unwrap(np.radians(fused))
    fused = np.degrees(fused)

    return fused



def compute_segment_angles(df):

    dt = df["dt"].values
    
    thigh_pitch = compute_segment_orientation(
    df["imu0_ax_f"].values,
    df["imu0_ay_f"].values,
    df["imu0_az_f"].values,
    df["imu0_gy_f"].values,
    dt,
    imu_name="imu0"
    )

    shank_pitch = compute_segment_orientation(
        df["imu1_ax_f"].values,
        df["imu1_ay_f"].values,
        df["imu1_az_f"].values,
        df["imu1_gx_f"].values,
        dt,
        imu_name="imu1"
    )

    return thigh_pitch, shank_pitch


# ==========================================================
# KNEE ANGLE (GEOMETRIC, VECTOR-BASED)
# ==========================================================

def compute_knee_angle(df, calibration_time=3.0):

    thigh_pitch, shank_pitch = compute_segment_angles(df)

    dt_mean = df["dt"].iloc[1:].mean()
    fs = 1.0 / dt_mean
    calib_samples = int(calibration_time * fs)

    # kalibracja (stanie)
    thigh_offset = np.mean(thigh_pitch[:calib_samples])
    shank_offset = np.mean(shank_pitch[:calib_samples])

    thigh_corr = thigh_pitch - thigh_offset
    shank_corr = shank_pitch - shank_offset

    # wektory 2D
    thigh_rad = np.radians(thigh_corr)
    shank_rad = np.radians(shank_corr)

    v_thigh = np.column_stack((np.sin(thigh_rad), np.cos(thigh_rad)))
    v_shank = np.column_stack((np.sin(shank_rad), np.cos(shank_rad)))

    dot = np.sum(v_thigh * v_shank, axis=1)
    dot = np.clip(dot, -1.0, 1.0)

    # ANATOMICZNA definicja
    knee_angle = 180 - np.degrees(np.arccos(dot))

    return knee_angle, thigh_corr, shank_corr

def debug_axes(df, calibration_time=3.0):

    dt_mean = df["dt"].iloc[1:].mean()
    fs = 1.0 / dt_mean
    calib_samples = int(calibration_time * fs)

    print("\n========== AXIS DEBUG ==========")

    print("\n--- IMU0 (THIGH) ---")
    print("Mean AX (standing):", np.mean(df["imu0_ax_f"].values[:calib_samples]))
    print("Mean AY (standing):", np.mean(df["imu0_ay_f"].values[:calib_samples]))
    print("Mean AZ (standing):", np.mean(df["imu0_az_f"].values[:calib_samples]))

    print("Full range AX:", df["imu0_ax_f"].min(), df["imu0_ax_f"].max())
    print("Full range AY:", df["imu0_ay_f"].min(), df["imu0_ay_f"].max())
    print("Full range AZ:", df["imu0_az_f"].min(), df["imu0_az_f"].max())

    print("\n--- IMU1 (SHANK) ---")
    print("Mean AX (standing):", np.mean(df["imu1_ax_f"].values[:calib_samples]))
    print("Mean AY (standing):", np.mean(df["imu1_ay_f"].values[:calib_samples]))
    print("Mean AZ (standing):", np.mean(df["imu1_az_f"].values[:calib_samples]))

    print("Full range AX:", df["imu1_ax_f"].min(), df["imu1_ax_f"].max())
    print("Full range AY:", df["imu1_ay_f"].min(), df["imu1_az_f"].max())
    print("Full range AZ:", df["imu1_az_f"].min(), df["imu1_az_f"].max())

    print("\n================================\n")