import cv2

def draw_reports(frame, angles, feedback_msgs, font_scale=0.6):

    for msg in feedback_msgs:
        if msg == "Za duze pochylenie tulowia":
            cv2.putText(
                frame,
                msg,
                (30, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
        if msg == "Zejdz nizej":
            cv2.putText(
                frame,
                msg,
                (30, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
        if msg == "Poprawna glebokosc":
            cv2.putText(
                frame,
                msg,
                (30, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )