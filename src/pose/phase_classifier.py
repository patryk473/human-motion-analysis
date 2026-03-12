import numpy as np
import pandas as pd


class PhaseClassifier:
    def __init__(self, fps, vel_threshold=5.0):
        """
        fps – liczba klatek na sekundę
        vel_threshold – próg prędkości kątowej (deg/s)
        """
        self.fps = fps
        self.vel_threshold = vel_threshold

    def classify(self, df):
        """
        df musi zawierać:
        - knee_angle
        - squat_id
        - time
        """

        df = df.copy()

        # ---------------------------------------
        # 1. Obliczenie prędkości kątowej
        # ---------------------------------------

        df["dtheta"] = df["knee_angle"].diff() * self.fps
        df["dtheta"] = df["dtheta"].fillna(0)

        df["phase_new"] = None

        # ---------------------------------------
        # 2. Klasyfikacja przez znak pochodnej
        # ---------------------------------------

        for i in range(1, len(df)):

            dtheta_prev = df.loc[i - 1, "dtheta"]
            dtheta_now = df.loc[i, "dtheta"]

            # BOTTOM – zmiana znaku z - na +
            if dtheta_prev < 0 and dtheta_now > 0:
                df.loc[i, "phase_new"] = "BOTTOM"

            elif dtheta_now < -self.vel_threshold:
                df.loc[i, "phase_new"] = "DESCENT"

            elif dtheta_now > self.vel_threshold:
                df.loc[i, "phase_new"] = "ASCENT"

            else:
                df.loc[i, "phase_new"] = "STABLE"

        # ---------------------------------------
        # 3. Phase percent (0–100%)
        # ---------------------------------------

        df["phase_percent_new"] = None

        for squat_id in df["squat_id"].dropna().unique():

            mask = df["squat_id"] == squat_id
            squat_df = df[mask]

            if len(squat_df) < 5:
                continue

            start_time = squat_df["time"].iloc[0]
            end_time = squat_df["time"].iloc[-1]

            total = end_time - start_time
            if total <= 0:
                continue

            percent = ((squat_df["time"] - start_time) / total) * 100
            df.loc[mask, "phase_percent_new"] = percent

        return df