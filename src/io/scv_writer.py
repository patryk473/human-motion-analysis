import pandas as pd
import os

def save_angles_csv(times, raw, smooth, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    df = pd.DataFrame({
        "time": times,
        "angle_raw": raw,
        "angle_smooth": smooth
    })

    df.to_csv(path, index=False)