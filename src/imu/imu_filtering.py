"""
IMU Filtering Module
------------------------------------------

Zadanie:
Usunięcie szumu wysokoczęstotliwościowego z sygnałów IMU.

Stosujemy:
- Filtr Butterwortha (low-pass)
- Zero-phase filtering (filtfilt)

Dlaczego?
Ruch biomechaniczny przysiadu mieści się zwykle w zakresie:
~0.5 – 3 Hz

Wszystko powyżej 6 Hz to głównie:
- szum czujnika
- mikrowibracje
- artefakty pomiarowe
"""

from scipy.signal import butter, filtfilt


# --------------------------------------------------
# LOWPASS FILTER
# --------------------------------------------------

def lowpass(signal, fs, cutoff=6, order=4):
    """
    Filtr dolnoprzepustowy Butterwortha.

    Parametry:
        signal  – sygnał wejściowy (1D array)
        fs      – częstotliwość próbkowania [Hz]
        cutoff  – częstotliwość odcięcia [Hz]
        order   – rząd filtra

    Zwraca:
        przefiltrowany sygnał (zero-phase)

    Dlaczego Butterworth?
    - płaska charakterystyka w paśmie przepustowym
    - dobre zachowanie dla danych biomechanicznych

    Dlaczego filtfilt?
    - filtracja w przód i w tył
    - brak przesunięcia fazowego
    - nie opóźnia sygnału (ważne dla analizy faz przysiadu)
    """

    # Normalizacja względem częstotliwości Nyquista
    # Nyquist = fs / 2
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist

    # Współczynniki filtra
    b, a = butter(order, normal_cutoff, btype="low")

    # Zero-phase filtering
    return filtfilt(b, a, signal)


# --------------------------------------------------
# FILTER IMU DATAFRAME
# --------------------------------------------------

def filter_imu(df, fs):
    """
    Nakłada filtr dolnoprzepustowy na wszystkie osie
    akcelerometru i żyroskopu dla obu IMU.

    Tworzy nowe kolumny:
        *_ax_f
        *_ay_f
        *_az_f
        *_gx_f
        *_gy_f
        *_gz_f

    Oryginalne dane pozostają bez zmian.
    """

    if fs <= 0:
        raise ValueError("Sampling frequency must be > 0")

    for imu in ["imu0", "imu1"]:
        for axis in ["x", "y", "z"]:

            # Filtrowanie akcelerometru
            df[f"{imu}_a{axis}_f"] = lowpass(
                df[f"{imu}_a{axis}"], fs
            )

            # Filtrowanie żyroskopu
            df[f"{imu}_g{axis}_f"] = lowpass(
                df[f"{imu}_g{axis}"], fs
            )

    return df
