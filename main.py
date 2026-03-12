import pandas as pd

from src.main import analyze_video
from src.io import save_angles_csv, plot_three_angles, save_squat_times_table, save_squat_report, save_squat_frames_csv, plot_quality_analysis
from src.pose import SquatEvaluator, PhaseClassifier, TimeNormalizer, SquatQualityScorer
times, angles, squats, squat_times, all_frames = analyze_video("data/raw/squat_analysis_imu_1.mp4")

plot_three_angles(times, angles,
                "Squat 02",
                "plots/squat_analysis_1_plot.png")

save_angles_csv(times, angles,
                "data/results/squat_analysis_1.csv")

# 4️⃣ CSV – FRAME-LEVEL (NAJWAŻNIEJSZE, POD IMU)
save_squat_frames_csv(all_frames,
        "data/results/squat_analysis_1_frames.csv"
    )
frames_path = "data/results/squat_analysis_1_frames.csv"
df = pd.read_csv(frames_path)
classifier = PhaseClassifier(fps=30)
df = classifier.classify(df)
df.to_csv("data/results/squat_analysis_1_frames_phases.csv", index=False)

df = pd.read_csv("data/results/squat_analysis_1_frames_phases.csv")
normalizer = TimeNormalizer(n_points=101)
df_norm = normalizer.normalize(df)
df_norm.to_csv("data/results/squat_analysis_1_normalized.csv", index=False)

df = pd.read_csv("data/results/squat_analysis_1_normalized.csv")
scorer = SquatQualityScorer()
scores = scorer.score_all(df)
scores.to_csv("data/results/squat_analysis_1_quality_scores.csv", index=False)

save_squat_times_table(squat_times, 
                       "data/results/squat_analysis_1_squats.csv")

evaluator = SquatEvaluator()
evaluated_squats = []

for squat in squats:
    evaluated_squats.append(evaluator.evaluate(squat))

save_squat_report(evaluated_squats, "data/results/squat_report_01.txt")

plot_quality_analysis(
    "data/results/squat_analysis_1_normalized.csv",
    "data/results/squat_analysis_1_quality_scores.csv"
)