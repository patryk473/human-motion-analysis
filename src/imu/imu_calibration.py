import json
import numpy as np


def apply_calibration(df, calib):
    """
    Zastosowanie kalibracji do surowych danych IMU.

    Co robi funkcja:

    1. Odejmuje offset akcelerometru (bias)
    2. Odejmuje offset żyroskopu (drift)
    3. Koryguje znaki osi (axis_sign), jeśli czujnik był obrócony

    Parametry:
        df     pandas DataFrame z surowymi danymi
        calib słownik wczytany z imu_calibration.json

    Zwraca:
        df  DataFrame z poprawionymi danymi
    """

    # Iterujemy po obu czujnikach
    for imu in ["imu0", "imu1"]:

        # ----------------------------
        # Pobranie parametrów kalibracji
        # ----------------------------

        acc_off = np.array(calib[imu]["acc_offset"])   # bias akcelerometru
        gyro_off = np.array(calib[imu]["gyro_offset"]) # bias żyroskopu
        sign = np.array(calib[imu]["axis_sign"])       # poprawka orientacji osi

        # ----------------------------
        # Korekcja każdej osi X,Y,Z
        # ----------------------------

        for i, axis in enumerate(["x", "y", "z"]):

            # AKCELEROMETR
            # 1. Odejmujemy bias
            # 2. Korygujemy znak osi
            df[f"{imu}_a{axis}"] = (
                df[f"{imu}_a{axis}"]
            ) * sign[i]

            # ŻYROSKOP
            # 1. Odejmujemy drift
            # 2. Korygujemy znak osi
            df[f"{imu}_g{axis}"] = (
                df[f"{imu}_g{axis}"] - gyro_off[i]
            ) * sign[i]

    return df