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
    
    biodro = pose_landmarks[hip]
    kolano = pose_landmarks[knee]
    kostka = pose_landmarks[ankle]
        
    A = np.array([biodro.x * w, biodro.y * h])
    B = np.array([kolano.x * w, kolano.y * h])
    C = np.array([kostka.x * w, kostka.y * h])

    return angle_3_points(A, B, C)

def hip_angle(pose_landmarks, w, h, side="left"):
    if side == "left":
        hip, knee, shoulder = 23, 25, 11
    else:
        hip, knee, shoulder = 24, 26, 12
    
    biodro = pose_landmarks[hip]
    kolano = pose_landmarks[knee]
    bark = pose_landmarks[shoulder]
        
    A = np.array([biodro.x * w, biodro.y * h])
    B = np.array([kolano.x * w, kolano.y * h])
    C = np.array([bark.x * w, bark.y * h])

    return angle_3_points(A, B, C)

def torso_tilt_angle(pose_landmarks, w, h, side="left"):
    if side == "left":
        hip, shoulder = 23, 11
    else:
        hip, shoulder = 24, 12
    
    biodro = pose_landmarks[hip]
    bark = pose_landmarks[shoulder]

    P_hip = np.array([biodro.x * w, biodro.y * h])
    P_shoulder = np.array([bark.x * w, bark.y * h])

    trunk_vec = P_shoulder - P_hip   # wektor tułowia
    vertical_vec = np.array([0, -1]) # wektor pionu obrazu

    trunk_norm = trunk_vec / np.linalg.norm(trunk_vec) # zrobienie żeby oba wektory miały długość jeden
    vertical_norm = vertical_vec / np.linalg.norm(vertical_vec) # zrobienie żeby oba wektory miały długość jeden

    cos_theta = np.dot(trunk_norm, vertical_norm) # iloczyn skalarny (wynik jest cosinusem kąta pomiędzy nimi, bo mają długość 1)
    cos_theta = np.clip(cos_theta, -1.0, 1.0) # zabezpieczenie: trzymaj się zakresu cosinusa

    angle_red = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_red)

    return angle_deg