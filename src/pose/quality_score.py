import numpy as np
import pandas as pd


class SquatQualityScorer:

    def __init__(self):
        self.w_rom = 0.35
        self.w_stability = 0.25
        self.w_tempo = 0.20
        self.w_trunk = 0.20

    def score_squat(self, squat_df):

        knee = squat_df["knee_angle_norm"].values
        trunk = squat_df["trunk_angle_norm"].values

        # --------------------
        # ROM
        # --------------------

        rom = np.max(knee) - np.min(knee)
        rom_score = min(100, (rom / 90) * 100)

        # --------------------
        # Stability
        # --------------------

        vel = np.diff(knee)
        sigma = np.std(vel)

        stability_score = max(0, 100 - sigma * 5)

        # --------------------
        # Tempo symmetry
        # --------------------

        bottom_idx = np.argmin(knee)

        descent = bottom_idx
        ascent = len(knee) - bottom_idx

        if ascent == 0:
            tempo_score = 0
        else:
            ratio = descent / ascent
            tempo_score = max(0, 100 - abs(1 - ratio) * 100)

        # --------------------
        # Trunk control
        # --------------------

        trunk_max = np.max(trunk)

        if trunk_max < 20:
            trunk_score = 100
        elif trunk_max > 35:
            trunk_score = 0
        else:
            trunk_score = 100 * (1 - (trunk_max - 20) / 15)

        # --------------------
        # Final score
        # --------------------

        final_score = (
            rom_score * self.w_rom
            + stability_score * self.w_stability
            + tempo_score * self.w_tempo
            + trunk_score * self.w_trunk
        )

        return {
            "ROM": rom_score,
            "Stability": stability_score,
            "Tempo": tempo_score,
            "Trunk": trunk_score,
            "Score": final_score
        }

    def score_all(self, df):

        results = []

        for squat_id in df["squat_id"].unique():

            squat_df = df[df["squat_id"] == squat_id]

            scores = self.score_squat(squat_df)

            scores["squat_id"] = squat_id

            results.append(scores)

        return pd.DataFrame(results)