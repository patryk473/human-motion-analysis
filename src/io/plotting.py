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

def plot_three_angles(times, angles, title, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, ax = plt.subplots(3, 1, figsize=(12,8), sharex=True)

    angle_names = ["knee", "hip", "trunk"]
    titles = {
        "knee": "Knee flexion angle",
        "hip": "Hip angle",
        "trunk": "Trunk tilt angle"
    }

    for i, name in enumerate(angle_names):
        ax[i].plot(times, angles[name]["raw"], label="raw", alpha=0.5)
        ax[i].plot(times, angles[name]["smooth"], label="smooth", linewidth=2)

        ax[i].set_ylabel("Angle [deg]")
        ax[i].set_title(titles[name])
        ax[i].grid(True)
        ax[i].legend()
    
    ax[-1].set_xlabel("Time [s]")
    
    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()