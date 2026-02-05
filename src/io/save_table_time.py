import pandas as pd
import os

# def save_angles_table(times, angles, squat_ids, output_path):
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     data = {
#         "time": times,
#         "squat_id": squat_ids
#     }

#     for joint, values in angles.items():
#         data[f"{joint}_raw"] = values["raw"]
#         data[f"{joint}_smooth"] = values["smooth"]

#     df = pd.DataFrame(data)
#     df.to_csv(output_path, index=False)

#     return df        

def save_squat_times_table(squat_times, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.DataFrame(squat_times)
    df.to_csv(output_path, index=False)
    return df