import numpy as np
import pandas as pd


class TimeNormalizer:
    def __init__(self, n_points=101):
        self.n_points = n_points

    def normalize(self, df):
        """
        df musi zawierać:
        - squat_id
        - phase_percent_new (0–100)
        - knee_angle
        - hip_angle
        - trunk_angle
        """

        normalized_rows = []

        target_grid = np.linspace(0, 100, self.n_points)

        for squat_id in df["squat_id"].dropna().unique():

            squat_df = df[df["squat_id"] == squat_id].copy()

            if len(squat_df) < 10:
                continue

            # usuwamy NaN
            squat_df = squat_df.dropna(subset=["phase_percent_new"])

            percent = squat_df["phase_percent_new"].values

            knee = squat_df["knee_angle"].values
            hip = squat_df["hip_angle"].values
            trunk = squat_df["trunk_angle"].values

            # interpolacja
            knee_interp = np.interp(target_grid, percent, knee)
            hip_interp = np.interp(target_grid, percent, hip)
            trunk_interp = np.interp(target_grid, percent, trunk)

            for i in range(self.n_points):
                normalized_rows.append({
                    "squat_id": squat_id,
                    "percent": target_grid[i],
                    "knee_angle_norm": knee_interp[i],
                    "hip_angle_norm": hip_interp[i],
                    "trunk_angle_norm": trunk_interp[i]
                })

        return pd.DataFrame(normalized_rows)