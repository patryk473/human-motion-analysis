import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_quality_analysis(normalized_csv, scores_csv):

    Path("plots").mkdir(exist_ok=True)

    df = pd.read_csv(normalized_csv)
    scores = pd.read_csv(scores_csv)

    # =============================
    # 1. Knee angle cycles
    # =============================

    plt.figure(figsize=(10,6))

    for squat_id in df["squat_id"].unique():
        squat = df[df["squat_id"] == squat_id]

        plt.plot(
            squat["percent"],
            squat["knee_angle_norm"],
            alpha=0.6,
            label=f"Squat {int(squat_id)}"
        )

    plt.legend()
    plt.xlabel("Squat cycle (%)")
    plt.ylabel("Knee angle (deg)")
    plt.title("Knee Angle Trajectories")
    plt.grid(True)

    plt.savefig("plots/knee_angle_cycles.png", dpi=300)
    plt.close()


    # =============================
    # 2. Mean squat curve
    # =============================

    mean_curve = df.groupby("percent")["knee_angle_norm"].mean()
    std_curve = df.groupby("percent")["knee_angle_norm"].std()

    percent = mean_curve.index

    plt.figure(figsize=(10,6))

    plt.plot(percent, mean_curve, label="Mean squat", linewidth=3)

    plt.fill_between(
        percent,
        mean_curve - std_curve,
        mean_curve + std_curve,
        alpha=0.3,
        label="±1 STD"
    )

    plt.xlabel("Squat cycle (%)")
    plt.ylabel("Knee angle (deg)")
    plt.title("Mean Squat Curve")
    plt.legend()
    plt.grid(True)

    plt.savefig("plots/mean_squat_curve.png", dpi=300)
    plt.close()


    # =============================
    # 3. Trunk angle cycles
    # =============================

    plt.figure(figsize=(10,6))

    for squat_id in df["squat_id"].unique():
        squat = df[df["squat_id"] == squat_id]

        plt.plot(
            squat["percent"],
            squat["trunk_angle_norm"],
            alpha=0.6,
            label=f"Squat {int(squat_id)}"
        )

    plt.legend()    

    plt.xlabel("Squat cycle (%)")
    plt.ylabel("Trunk angle (deg)")
    plt.title("Trunk Angle Trajectories")
    plt.grid(True)

    plt.savefig("plots/trunk_angle_cycles.png", dpi=300)
    plt.close()


    # =============================
    # 4. Quality score plot
    # =============================

    plt.figure(figsize=(8,6))

    plt.bar(scores["squat_id"], scores["Score"])

    plt.xlabel("Squat ID")
    plt.ylabel("Quality Score")
    plt.title("Squat Quality Score (0–100)")
    plt.ylim(0,100)

    plt.grid(axis="y")

    plt.savefig("plots/quality_scores.png", dpi=300)
    plt.close()


    # =============================
    # 5. ROM distribution
    # =============================

    rom = []

    for squat_id in df["squat_id"].unique():
        squat = df[df["squat_id"] == squat_id]
        rom.append(
            squat["knee_angle_norm"].max() -
            squat["knee_angle_norm"].min()
        )

    plt.figure(figsize=(8,6))

    plt.hist(rom, bins=10)

    plt.xlabel("ROM (deg)")
    plt.ylabel("Count")
    plt.title("Range of Motion Distribution")

    plt.grid(True)

    plt.savefig("plots/rom_distribution.png", dpi=300)
    plt.close()


    print("✅ Plots saved to /plots/")