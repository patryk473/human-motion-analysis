import cv2

def draw_connections(frame, pose_landmarks, connections, w, h, color=(255,0,0)):
    for start_idx, end_idx in connections:
        p1 = pose_landmarks[start_idx]
        p2 = pose_landmarks[end_idx]

        x1, y1 = int(p1.x * w), int(p1.y * h)
        x2, y2 = int(p2.x * w), int(p2.y * h)

        cv2.line(frame, (x1,y1), (x2,y2), color, 2)

def draw_points(frame, pose_landmarks, indices, w, h, color=(0,255,0)):
    for idx in indices:
        landmark = pose_landmarks[idx]
        x = int(landmark.x * w)
        y = int(landmark.y * h)

        cv2.circle(frame, (x,y), 4, color, -1)
