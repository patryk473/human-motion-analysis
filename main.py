from src.main import analyze_video
from src.io import plot_knee_angle
from src.io import save_angles_csv

times, raw, smooth = analyze_video("data/raw/knee_flexion_01.mp4")

plot_knee_angle(times, raw, smooth,
                "Zgięcie kolana 01",
                "plots/knee_flexion_01_plot(1).png")

save_angles_csv(times, raw, smooth,
                "data/results/knee_flexion.csv")
