"""
IMU calibration script
------------------------------------------

Co robi ten plik?

1. Liczy offset akcelerometru (bias)
2. Liczy offset żyroskopu (drift)
3. Automatycznie wykrywa czy któryś IMU jest obrócony (axis_sign)
4. Zapisuje wszystko do JSON

Usage:
python src/imu/calibrate_imu.py path/to/imu_session_raw.csv
"""

import sys
import json
import itertools  # potrzebne do generowania kombinacji znaków ±1
from pathlib import Path

import pandas as pd
import numpy as np


# --------------------------------------------------
# AUTO AXIS DETECTION
# --------------------------------------------------

def auto_detect_axis_sign(g_ref: np.ndarray, g_target: np.ndarray):
    """
    Automatycznie znajduje kombinację znaków [±1, ±1, ±1],
    która maksymalizuje wyrównanie dwóch wektorów grawitacji.

    g_ref      wektor referencyjny (np. imu0)
    g_target   wektor który chcemy dopasować (np. imu1)

    Zwraca:
        best_sign  lista np. [-1, -1, 1]
        best_dot   wartość iloczynu skalarnego (diagnostyka)
    """

    best_sign = None        # najlepsza kombinacja znaków
    best_dot = -np.inf      # największy znaleziony iloczyn skalarny

    # Generujemy wszystkie 8 możliwych kombinacji znaków
    # (-1 lub +1 dla każdej osi X,Y,Z)
    for signs in itertools.product([-1, 1], repeat=3):

        sign_vec = np.array(signs)

        # Mnożymy wektor przez kombinację znaków
        corrected = g_target * sign_vec

        # Liczymy iloczyn skalarny (miara zgodności kierunku)
        dot = np.dot(g_ref, corrected)

        # Jeśli lepszy niż poprzedni → zapisujemy
        if dot > best_dot:
            best_dot = dot
            best_sign = sign_vec

    return best_sign.tolist(), best_dot


# --------------------------------------------------
# GŁÓWNA FUNKCJA KALIBRACJI
# --------------------------------------------------

def calibrate_offsets(raw_csv_path: str, duration_s: float = 5.0):

    # Zamiana ścieżki na obiekt Path
    raw_csv_path = Path(raw_csv_path)

    # Sprawdzenie czy plik istnieje
    if not raw_csv_path.exists():
        raise FileNotFoundError(raw_csv_path)

    print(f"\n[CAL] Loading RAW file: {raw_csv_path}")

    # Wczytanie CSV do DataFrame
    df = pd.read_csv(raw_csv_path)

    # Sprawdzenie czy mamy timestamp
    if "ts" not in df.columns:
        raise ValueError("Column 'ts' not found in CSV")

    # --------------------------------------------------
    # WYCIĘCIE PIERWSZYCH X SEKUND (zakładamy: stoisz nieruchomo)
    # --------------------------------------------------

    t0 = df["ts"].iloc[0]  # pierwszy timestamp

    # Bierzemy tylko pierwsze duration_s sekund
    df = df[df["ts"] <= t0 + duration_s * 1000]

    print(f"[CAL] Using first {duration_s} seconds for calibration")
    print(f"[CAL] Samples used: {len(df)}")

    calib = {}              # słownik do zapisania wyników
    gravity_vectors = {}    # do detekcji osi


    # --------------------------------------------------
    # LICZENIE OFFSETÓW DLA KAŻDEGO IMU
    # --------------------------------------------------

    for imu in ["imu0", "imu1"]:

        # --- AKCELEROMETR ---
        acc = np.vstack([
            df[f"{imu}_ax"],
            df[f"{imu}_ay"],
            df[f"{imu}_az"]
        ]).T

        # --- ŻYROSKOP ---
        gyro = np.vstack([
            df[f"{imu}_gx"],
            df[f"{imu}_gy"],
            df[f"{imu}_gz"]
        ]).T

        # Średnia wartość = offset czujnika
        acc_mean = acc.mean(axis=0)
        gyro_mean = gyro.mean(axis=0)

        # Zapisujemy średni wektor grawitacji
        gravity_vectors[imu] = acc_mean.copy()

        calib[imu] = {
            "acc_offset": acc_mean.tolist(),   # bias akcelerometru
            "gyro_offset": gyro_mean.tolist(), # drift żyroskopu
            "axis_sign": [1, 1, 1]             # tymczasowo (zmienimy później)
        }

        print(f"\n[CAL] {imu}")
        print(f"      acc_offset  = {acc_mean}")
        print(f"      gyro_offset = {gyro_mean}")
        print(f"      |g|         = {np.linalg.norm(acc_mean):.3f}")
        # |g| powinno być ~9.81


    # --------------------------------------------------
    # AUTOMATYCZNA DETEKCJA FLIPU OSI
    # --------------------------------------------------

    print("\n[CAL] Detecting axis alignment...")

    g0 = gravity_vectors["imu0"]  # referencja
    g1 = gravity_vectors["imu1"]  # dopasowywany

    axis_sign_imu1, dot_value = auto_detect_axis_sign(g0, g1)

    # imu0 zostaje referencją
    calib["imu0"]["axis_sign"] = [1, 1, 1]
    calib["imu1"]["axis_sign"] = axis_sign_imu1

    print(f"[CAL] Best axis_sign for imu1: {axis_sign_imu1}")
    print(f"[CAL] Alignment dot product : {dot_value:.3f}")


    # --------------------------------------------------
    # ZAPIS DO JSON
    # --------------------------------------------------

    out = Path("data/config/imu_calibration.json")
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w") as f:
        json.dump(calib, f, indent=2)

    print(f"\n[CAL] Calibration saved to {out}")
    print("[CAL] Done.\n")


# --------------------------------------------------
# CLI (wywołanie z terminala)
# --------------------------------------------------

if __name__ == "__main__":

    # Jeśli nie podano ścieżki
    if len(sys.argv) < 2:
        print("Usage:")
        print("python src/imu/calibrate_imu.py path/to/imu_session_raw.csv")
        sys.exit(1)

    calibrate_offsets(sys.argv[1])
