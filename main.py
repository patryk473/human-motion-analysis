from src.main import analyze_video
from src.io import save_angles_csv, plot_three_angles, save_squat_times_table, save_squat_report, save_squat_frames_csv
from src.pose import SquatEvaluator

times, angles, squats, squat_times, all_frames = analyze_video("data/raw/squat_02.mp4")

plot_three_angles(times, angles,
                "Squat 02",
                "plots/squat_02_plot.png")

save_angles_csv(times, angles,
                "data/results/squat_02.csv")

# 4️⃣ CSV – FRAME-LEVEL (NAJWAŻNIEJSZE, POD IMU)
save_squat_frames_csv(all_frames,
        "data/results/squat_02_frames.csv"
    )

save_squat_times_table(squat_times, 
                       "data/results/squat_02_squats.csv")

evaluator = SquatEvaluator()
evaluated_squats = []

for squat in squats:
    evaluated_squats.append(evaluator.evaluate(squat))

save_squat_report(evaluated_squats, "data/results/squat_report_02.txt")