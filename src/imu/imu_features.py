import numpy as np
import pandas as pd


def compute_features(df, window_size=10):
    """
    Ekstrakcja cech (features) z przefiltrowanych danych IMU.

    Zakładamy, że df zawiera już:
        *_ax_f, *_ay_f, *_az_f  → filtrowany akcelerometr
        *_gx_f, *_gy_f, *_gz_f  → filtrowany żyroskop

    Parametry:
        df          – DataFrame z danymi po kalibracji i filtracji
        window_size – liczba próbek w jednym oknie analizy

    Zwraca:
        DataFrame z cechami dla każdego okna i każdego IMU

    Pipeline:
        sygnał ciągły → podział na okna → cechy statystyczne
    """

    rows = []  # lista słowników (każdy wiersz = jedno okno)


    # --------------------------------------------------
    # Iterujemy po obu czujnikach
    # --------------------------------------------------

    for imu in ["imu0", "imu1"]:

        # --------------------------------------------------
        # MODUŁ (norma) przyspieszenia
        # --------------------------------------------------
        # Liczymy normę wektora:
        # sqrt(ax² + ay² + az²)
        #
        # Dlaczego?
        # - eliminuje zależność od osi
        # - daje ogólną "intensywność ruchu"
        # - odporne na niewielkie błędy orientacji

        acc = np.sqrt(
            df[f"{imu}_ax_f"]**2 +
            df[f"{imu}_ay_f"]**2 +
            df[f"{imu}_az_f"]**2
        )

        # --------------------------------------------------
        # MODUŁ prędkości kątowej
        # --------------------------------------------------
        # sqrt(gx² + gy² + gz²)
        #
        # Reprezentuje ogólną intensywność rotacji segmentu.

        gyro = np.sqrt(
            df[f"{imu}_gx_f"]**2 +
            df[f"{imu}_gy_f"]**2 +
            df[f"{imu}_gz_f"]**2
        )

        # --------------------------------------------------
        # Sliding window (bez overlap)
        # --------------------------------------------------
        # Dzielimy sygnał na bloki po window_size próbek.
        #
        # Każde okno daje jedną paczkę cech.

        for i in range(0, len(df) - window_size, window_size):

            acc_window = acc[i:i+window_size]
            gyro_window = gyro[i:i+window_size]

            rows.append({

                # który IMU (udo / łydka)
                "imu": imu,

                # zakres czasowy okna
                "t_start": df["ts"].iloc[i],
                "t_end": df["ts"].iloc[i + window_size - 1],

                # --------------------------------------------------
                # ACC FEATURES
                # --------------------------------------------------

                # RMS = Root Mean Square
                # mierzy "energię" sygnału
                # bardziej czułe na duże wartości niż zwykła średnia
                "acc_rms": np.sqrt(np.mean(acc_window**2)),

                # Wariancja = miara zmienności sygnału
                # wysoka przy dynamicznym ruchu
                "acc_var": np.var(acc_window),

                # --------------------------------------------------
                # GYRO FEATURES
                # --------------------------------------------------

                # RMS prędkości kątowej
                # dobra miara intensywności rotacji
                "gyro_rms": np.sqrt(np.mean(gyro_window**2)),

                # zmienność rotacji
                "gyro_var": np.var(gyro_window),

                # maksymalna bezwzględna prędkość kątowa w oknie
                # dobra do wykrywania dynamicznych faz (np. wstawanie)
                "gyro_peak": np.max(np.abs(gyro_window))
            })

    return pd.DataFrame(rows)
