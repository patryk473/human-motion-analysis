import matplotlib.pyplot as plt
import os

def plot_knee_angle(times, raw, smooth, title, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(10,5))
    plt.plot(times, raw, label="kąt surowy", alpha = 0.4)
    plt.plot(times, smooth, label="kąt wygładzony", linewidth=2)

    plt.xlabel("Czas [s]")
    plt.ylabel("Kąt kolana [°]")
    plt.title("Zgięcie kolana 01")
    plt.legend()
    plt.grid(True)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()