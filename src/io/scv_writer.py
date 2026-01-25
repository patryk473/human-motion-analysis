import pandas as pd
import os

def save_angles_csv(times, angles, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    df = pd.DataFrame({
        "time": times,
        "knee_raw": angles["knee"]["raw"],
        "knee_smooth": angles["knee"]["smooth"],
        "hip_raw": angles["hip"]["raw"],
        "hip_smooth": angles["hip"]["smooth"],
        "trunk_raw": angles["trunk"]["raw"],
        "trunk_smooth": angles["trunk"]["smooth"],
    })

    df.to_csv(path, index=False)