import cv2

def draw_angles(frame, angles, font_scale=0.6):
    
    def fmt(val):
        return f"{val:.1f}" if val is not None else "--"
    
    cv2.putText(
        frame,
        f"Knee:  {fmt(angles['knee']['smooth'][-1])}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Hip:   {fmt(angles['hip']['smooth'][-1])}",
        (30, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Trunk: {fmt(angles['trunk']['smooth'][-1])}",
        (30, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (0, 255, 255),
        2
    )