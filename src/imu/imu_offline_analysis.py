import pandas as pd
import numpy as np
from pathlib import Path
from scipy.signal import correlate


# =========================================
# 1. NORMALIZE TIME
# =========================================

def normalize_time(df):
    df["time_s"] = (df["ts"] - df["ts"].iloc[0]) / 1000.0
    return df


# =========================================
# 2. COMPLEMENTARY FILTER (POPRAWNY)
# =========================================

def complementary_filter(acc_angle, gyro_rate, dt, alpha=0.97):

    fused = np.zeros_like(acc_angle)
    fused[0] = acc_angle[0]

    for i in range(1, len(acc_angle)):

        predicted = fused[i-1] + gyro_rate[i] * dt[i]

        error = acc_angle[i] - predicted
        error = (error + 180) % 360 - 180

        fused[i] = predicted + (1 - alpha) * error

    return fused


# =========================================
# 3. COMPUTE SEGMENT ORIENTATION
# =========================================

def compute_segment_orientation(ax, ay, az, gyro_axis, dt):

    # normalizacja akcelerometru
    norm = np.sqrt(ax**2 + ay**2 + az**2)
    ax = ax / norm
    ay = ay / norm
    az = az / norm

    # pitch względem pionu (dopasowane do Twojego montażu)
    acc_angle = np.degrees(np.arctan2(ax, -ay))

    fused = complementary_filter(acc_angle, gyro_axis, dt)

    return fused


# =========================================
# 4. COMPUTE TRUE KNEE ANGLE
# =========================================

def compute_knee_angle(df, calibration_time=3.0):

    dt = df["dt"].values

    thigh_pitch = compute_segment_orientation(
        df["imu0_ax_f"].values,
        df["imu0_ay_f"].values,
        df["imu0_az_f"].values,
        df["imu0_gy_f"].values,
        dt
    )

    shank_pitch = compute_segment_orientation(
        df["imu1_ax_f"].values,
        df["imu1_ay_f"].values,
        df["imu1_az_f"].values,
        df["imu1_gy_f"].values,
        dt
    )

    # unwrap
    thigh_pitch = np.degrees(np.unwrap(np.radians(thigh_pitch)))
    shank_pitch = np.degrees(np.unwrap(np.radians(shank_pitch)))

    # kalibracja stania
    fs = 1.0 / np.mean(dt[1:])
    calib_samples = int(calibration_time * fs)

    thigh_pitch -= np.mean(thigh_pitch[:calib_samples])
    shank_pitch -= np.mean(shank_pitch[:calib_samples])

    # wektory 2D
    thigh_rad = np.radians(thigh_pitch)
    shank_rad = np.radians(shank_pitch)

    v_thigh = np.column_stack((np.sin(thigh_rad), np.cos(thigh_rad)))
    v_shank = np.column_stack((np.sin(shank_rad), np.cos(shank_rad)))

    dot = np.sum(v_thigh * v_shank, axis=1)
    dot = np.clip(dot, -1.0, 1.0)

    knee_angle = 180 - np.degrees(np.arccos(dot))

    df["knee_angle_imu"] = knee_angle
    df["thigh_pitch"] = thigh_pitch
    df["shank_pitch"] = shank_pitch

    return df


# =========================================
# 5. OFFLINE PIPELINE
# =========================================

def process_imu_offline(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    df = normalize_time(df)
    df = compute_knee_angle(df)

    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    print("✅ IMU offline analysis saved:", output_csv)

# =========================================
# 6. SYNCHRONIZATION (CROSS-CORRELATION)
# =========================================

def synchronize_imu_video(video_csv, imu_csv, output_csv):

    video = pd.read_csv(video_csv)
    imu = pd.read_csv(imu_csv)

    v_time = video["time"].values
    i_time = imu["time_s"].values

    v_angle = video["knee_angle"].values
    i_angle = imu["knee_angle_imu"].values

    # -----------------------------------------
    # IGNORUJEMY PIERWSZE 2 SEKUNDY (start)
    # -----------------------------------------

    start_offset = 2.0

    v_mask = v_time > start_offset
    i_mask = i_time > start_offset

    v_min_idx = np.argmin(v_angle[v_mask])
    i_min_idx = np.argmin(i_angle[i_mask])

    v_min_time = v_time[v_mask][v_min_idx]
    i_min_time = i_time[i_mask][i_min_idx]

    # -----------------------------------------
    # PRZESUNIĘCIE
    # -----------------------------------------

    time_shift = v_min_time - i_min_time

    print(f"🔁 Synchronizacja po pierwszym minimum: {time_shift:.3f} s")

    imu["time_s_sync"] = imu["time_s"] + time_shift

    # -----------------------------------------
    # INTERPOLACJA
    # -----------------------------------------

    imu_interp = np.interp(
        video["time"].values,
        imu["time_s_sync"],
        imu["knee_angle_imu"],
        left=np.nan,
        right=np.nan
    )

    synced = video.copy()
    synced["knee_angle_imu_sync"] = imu_interp

    synced = synced.dropna(subset=["knee_angle_imu_sync"])

    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    synced.to_csv(output_csv, index=False)

    print("✅ Zapisano zsynchronizowany plik:", output_csv)