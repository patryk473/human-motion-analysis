from src.main import analyze_video
from src.io import save_angles_csv, plot_three_angles, save_angles_table, save_squat_times_table

times, angles, squat_times, frame_squat_ids = analyze_video("data/raw/squat_02.mp4")

plot_three_angles(times, angles,
                "Squat 02",
                "plots/squat_02_plot.png")

save_angles_csv(times, angles,
                "data/results/squat_02.csv")

save_angles_table(times, angles, frame_squat_ids,
                  "data/results/squat_02_table.csv")

save_squat_times_table(squat_times, 
                       "data/results/squat_02_squats.csv")
