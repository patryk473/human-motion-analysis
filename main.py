from src.main import analyze_video
from src.io import save_angles_csv
from src.io import plot_three_angles

times, angles = analyze_video("data/raw/squat_02.mp4")

plot_three_angles(times, angles,
                "Squat 02",
                "plots/squat_02_plot.png")

save_angles_csv(times, angles,
                "data/results/squat_02.csv")
