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