from enum import Enum

class SquatState(Enum):
    STANDING = 0
    DESCENDING = 1
    BOTTOM = 2
    ASCENDING = 3
    FAIL = 4

class SquatDetector:
    def __init__(self, fps):
        self.state = SquatState.STANDING
        self.prev_angle = None
        self.fps = fps
        self.current_squat = {}
        self.squats = []
        self.active_squat_id = 0

    def update(self, angle, frame_idx):
        ANGLE_START = 160
        ANGLE_BOTTOM = 90
        ANGLE_STAND = 165
        MIN_SQUAT_DEPTH = 120

        if self.state == SquatState.STANDING:
            if angle < ANGLE_START:
                self.active_squat_id += 1
                self.state = SquatState.DESCENDING
                self.current_squat = {
                    "start_frame": frame_idx,
                    "angles": [],
                    "min_angle": 999
                }

        elif self.state == SquatState.DESCENDING:
            self.current_squat["angles"].append(angle)
            self.current_squat["min_angle"] = min(self.current_squat["min_angle"], angle)
            if angle < ANGLE_BOTTOM:
                self.state = SquatState.BOTTOM
                self.current_squat["bottom_frame"] = frame_idx
            if self.prev_angle and angle > self.prev_angle and self.current_squat["min_angle"] > 140:
                self.state = SquatState.STANDING
                self.active_squat_id -= 1
                self.current_squat = {}

        elif self.state == SquatState.BOTTOM:
            self.current_squat["angles"].append(angle)
            self.current_squat["min_angle"] = min(self.current_squat["min_angle"], angle)
            if self.prev_angle and angle > self.prev_angle:
                self.state = SquatState.ASCENDING

        elif self.state == SquatState.ASCENDING:
            self.current_squat["angles"].append(angle)
            self.current_squat["min_angle"] = min(self.current_squat["min_angle"], angle)
            if angle > ANGLE_STAND:
                self.state = SquatState.STANDING

                if self.current_squat["min_angle"] < MIN_SQUAT_DEPTH:
                    self.current_squat["end_frame"] = frame_idx
                    self.squats.append(self.current_squat)
                else:
                    pass
            
                self.current_squat = {}

            # if angle < ANGLE_BOTTOM:
            #     self.state = SquatState.FAIL
            #     self.active_squat_id -= 1
            #     self.current_squat = {}

        # elif self.state == SquatState.FAIL:
        #     if angle > ANGLE_STAND:
        #         self.state = SquatState.STANDING

        self.prev_angle = angle

    def get_squats(self):
        return self.squats
    
    def compute_times(self):
        results = []

        for i, squat in enumerate(self.squats):
            if not all(k in squat for k in ["start_frame", "bottom_frame", "end_frame"]):
                continue
            
            descent = (squat["bottom_frame"] - squat["start_frame"]) 
            ascent  = (squat["end_frame"] - squat["bottom_frame"]) 
            total   = (squat["end_frame"] - squat["start_frame"]) 

            results.append({
                "squat_id": i + 1,
                "descent_time": descent,
                "ascent_time": ascent,
                "total_time": total,
                "tempo_ratio": descent / ascent if ascent > 0 else None
            })
    
        return results