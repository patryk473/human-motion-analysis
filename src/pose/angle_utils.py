import numpy as np

def angle_3_points(A, B, C):
    BA = A - B
    BC = C - B

    cosine = np.dot(BA, BC) / (
        np.linalg.norm(BA) * np.linalg.norm(BC)
    )

    # zabezpieczenie numeryczne
    cosine = np.clip(cosine, -1.0, 1.0)

    angle = np.degrees(np.arccos(cosine))
    return angle

def knee_flexion_angle(pose_landmarks, w, h, side="left"):
    if side == "left":
        hip, knee, ankle = 23, 25, 27
    else:
        hip, knee, ankle = 24, 26, 28
    
    biodro = pose_landmarks[23]
    kolano = pose_landmarks[25]
    kostka = pose_landmarks[27]
        
    A = np.array([biodro.x * w, biodro.y * h])
    B = np.array([kolano.x * w, kolano.y * h])
    C = np.array([kostka.x * w, kostka.y * h])

    return angle_3_points(A, B, C)
