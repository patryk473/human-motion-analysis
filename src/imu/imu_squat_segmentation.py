import numpy as np
import pandas as pd
from scipy.signal import find_peaks


def segment_imu_squats(df,
                       knee_col="knee_angle_imu",
                       time_col="time_s",
                       min_depth=130,
                       min_distance_s=1.5):
    """
    Segmentacja przysiadów z IMU.

    Definicja cyklu:
        max → min → max

    Parametry:
        min_depth      – minimalna głębokość przysiadu
        min_distance_s – minimalny czas między squatami

    Zwraca:
        df z kolumnami:
            imu_squat_id
            imu_phase
    """

    df = df.copy()

    knee = df[knee_col].values
    time = df[time_col].values

    # --------------------------------------------------
    # sampling frequency
    # --------------------------------------------------

    dt = np.mean(np.diff(time))
    fs = 1.0 / dt

    min_distance = int(min_distance_s * fs)

    # --------------------------------------------------
    # DETEKCJA MINIMUM (BOTTOM)
    # --------------------------------------------------

    minima, _ = find_peaks(
        -knee,
        distance=min_distance,
        prominence=15
    )

    # --------------------------------------------------
    # DETEKCJA MAXIMUM
    # --------------------------------------------------

    maxima, _ = find_peaks(
        knee,
        distance=min_distance,
        prominence=5
    )

    df["imu_squat_id"] = np.nan
    df["imu_phase"] = None

    squat_id = 1

    for m in minima:

        # --------------------------------------------------
        # znajdź poprzednie maksimum (start)
        # --------------------------------------------------

        prev_max = maxima[maxima < m]

        if len(prev_max) == 0:
            continue

        start = prev_max[-1]

        # --------------------------------------------------
        # znajdź następne maksimum (end)
        # --------------------------------------------------

        next_max = maxima[maxima > m]

        if len(next_max) == 0:
            continue

        end = next_max[0]

        # --------------------------------------------------
        # sprawdź głębokość
        # --------------------------------------------------

        depth = knee[start] - knee[m]

        if depth < min_depth:
            continue

        # --------------------------------------------------
        # zapis squat_id
        # --------------------------------------------------

        df.loc[start:end, "imu_squat_id"] = squat_id

        # --------------------------------------------------
        # fazy
        # --------------------------------------------------

        df.loc[start:m, "imu_phase"] = "descent"
        df.loc[m:end, "imu_phase"] = "ascent"

        squat_id += 1

    return df