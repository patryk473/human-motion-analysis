"""
IMU processing pipeline
------------------------------------------

Pipeline przetwarzania danych IMU:

RAW CSV
    ↓
Kalibracja (offset + axis correction)
    ↓
Filtrowanie (low-pass)
    ↓
Ekstrakcja cech (features)
    ↓
Zapis CSV

Usage:
python src/imu/process_imu.py path/to/imu_session_xxx.csv
"""

import sys
import json
from pathlib import Path

import pandas as pd
import numpy as np

from .imu_calibration import apply_calibration
from .imu_filtering import filter_imu
from .imu_features import compute_features


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def estimate_fs(df):
    """
    Estimate sampling frequency from dt column.
    Ignores first sample (dt = 0).
    """

    if "dt" not in df.columns:
        raise ValueError("CSV must contain 'dt' column")

    # Pomijamy pierwszą próbkę (dt = 0)
    dt_values = df["dt"].iloc[1:]

    if (dt_values <= 0).any():
        raise ValueError("Invalid dt values detected (after first sample)")

    mean_dt = dt_values.mean()

    return 1.0 / mean_dt



# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def process_imu_file(raw_csv_path: str):

    raw_csv_path = Path(raw_csv_path)

    if not raw_csv_path.exists():
        raise FileNotFoundError(raw_csv_path)

    print(f"\n[IMU] Loading RAW file: {raw_csv_path}")
    df_raw = pd.read_csv(raw_csv_path)

    # --------------------------------------------------
    # Sampling frequency
    # --------------------------------------------------

    fs = estimate_fs(df_raw)
    print(f"[IMU] Estimated sampling frequency: {fs:.2f} Hz")

    # --------------------------------------------------
    # Calibration
    # --------------------------------------------------

    calib_path = Path("data/config/imu_calibration.json")

    if not calib_path.exists():
        raise FileNotFoundError(
            "Missing calibration file: data/config/imu_calibration.json\n"
            "Run calibrate_imu.py first."
        )

    with open(calib_path, "r") as f:
        calib = json.load(f)

    print("[IMU] Applying calibration (offset + axis correction)")

    # copy() żeby nie modyfikować oryginalnych danych
    df_cal = apply_calibration(df_raw.copy(), calib)

    # --------------------------------------------------
    # Filtering
    # --------------------------------------------------

    print("[IMU] Applying low-pass filtering")

    # Filtr usuwa:
    # - szum wysokoczęstotliwościowy
    # - mikrodrgania
    # - artefakty pomiarowe

    df_filt = filter_imu(df_cal.copy(), fs)

    # --------------------------------------------------
    # Output paths
    # --------------------------------------------------

    session_name = raw_csv_path.stem.replace("imu_session_", "")

    out_filtered = Path("data/result_imu/filtered") / f"{session_name}_filtered.csv"
    out_features = Path("data/result_imu/features") / f"{session_name}_features.csv"

    out_filtered.parent.mkdir(parents=True, exist_ok=True)
    out_features.parent.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # Save FILTERED
    # --------------------------------------------------

    print(f"[IMU] Saving filtered CSV: {out_filtered}")
    df_filt.to_csv(out_filtered, index=False)

    # --------------------------------------------------
    # Feature extraction
    # --------------------------------------------------

    print("[IMU] Computing features")

    # Tu liczysz np:
    # - kąt kolana
    # - prędkość kątową
    # - tempo
    # - zakres ruchu
    # - inne wskaźniki biomechaniczne

    df_feat = compute_features(df_filt)

    print(f"[IMU] Saving features CSV: {out_features}")
    df_feat.to_csv(out_features, index=False)

    print("[IMU] DONE\n")

    return out_filtered, out_features


# --------------------------------------------------
# CLI
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python src/imu/process_imu.py path/to/imu_session_xxx.csv")
        sys.exit(1)

    process_imu_file(sys.argv[1])
