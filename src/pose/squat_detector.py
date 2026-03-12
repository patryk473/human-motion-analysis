from enum import Enum

class SquatState(Enum):
    STANDING = 0
    DESCENDING = 1
    BOTTOM = 2
    ASCENDING = 3
    FAIL = 4

class SquatPhase(Enum):
    START = 0
    DESCENT = 1
    BOTTOM = 2
    ASCENT = 3
    END = 4

class SquatDetector:
    ASCENT_DELTA = 1.0
    BOTTOM_ENTER = 95
    def __init__(self, fps):
        self.state = SquatState.STANDING
        self.prev_angle = None
        self.fps = fps
        self.current_squat = {}
        self.squats = []
        self.next_squat_id = 1
        self.current_phase = None

    def update(self, knee_angle, trunk_angle, time_s, frame_index):
        ANGLE_START = 160
        ANGLE_BOTTOM = 90
        ANGLE_STAND = 165
        MIN_SQUAT_DEPTH = 120

        if self.state != SquatState.STANDING and self.current_squat:
            phase = self._state_to_phase()
            self.current_squat["frames"].append({
                "frame": frame_index,  
                "time": time_s,
                "knee_angle": knee_angle,
                "trunk_angle": trunk_angle,
                "hip_angle": None, 
                "state": self.state.name,
                "phase": phase.name if phase else None,
                "squat_id": self.current_squat["squat_id"]
            })

        if self.state == SquatState.STANDING:
            if knee_angle < ANGLE_START and self.prev_angle and knee_angle < self.prev_angle:
                self.current_phase = SquatPhase.START
                self.state = SquatState.DESCENDING

                self.current_squat = {
                    "squat_id": self.next_squat_id,
                    "start_time": time_s,
                    "bottom_time": None,
                    "end_time": None,
                    "min_knee": 999,
                    "max_trunk": 0,
                    "frames": []
                }
                self.next_squat_id += 1

                # START FRAME – tylko raz
                self.current_squat["frames"].append({
                    "frame": frame_index,
                    "time": time_s,
                    "knee_angle": knee_angle,
                    "trunk_angle": trunk_angle,
                    "hip_angle": None,
                    "state": self.state.name,
                    "phase": SquatPhase.START.name,
                    "squat_id": self.current_squat["squat_id"]
                })
                
        elif self.state == SquatState.DESCENDING:
            self.current_squat["min_knee"] = min(self.current_squat["min_knee"], knee_angle)
            self.current_squat["max_trunk"] = max(self.current_squat["max_trunk"], trunk_angle)
            if knee_angle < self.BOTTOM_ENTER:
                self.state = SquatState.BOTTOM
                self.current_phase = SquatPhase.BOTTOM
                self.current_squat["bottom_time"] = time_s
            if self.prev_angle and knee_angle > self.prev_angle and self.current_squat["min_knee"] > 140:
                self.state = SquatState.STANDING
                self.current_squat = {}

        elif self.state == SquatState.BOTTOM:
            self.current_squat["min_knee"] = min(self.current_squat["min_knee"], knee_angle)
            self.current_squat["max_trunk"] = max(self.current_squat["max_trunk"], trunk_angle)
            if self.prev_angle and (knee_angle - self.prev_angle) > self.ASCENT_DELTA:
                self.state = SquatState.ASCENDING
                self.current_phase = SquatPhase.ASCENT

        elif self.state == SquatState.ASCENDING:
            self.current_squat["min_knee"] = min(self.current_squat["min_knee"], knee_angle)
            self.current_squat["max_trunk"] = max(self.current_squat["max_trunk"], trunk_angle)
            if knee_angle > ANGLE_STAND:
                self.state = SquatState.STANDING
                self.current_phase = SquatPhase.END

                if self.current_squat["min_knee"] < MIN_SQUAT_DEPTH:
                    self.current_squat["end_time"] = time_s
                    self.squats.append(self.current_squat)
                else:
                    pass
            
                self.current_squat = {}

        self.prev_angle = knee_angle

    def _state_to_phase(self):
        if self.state == SquatState.DESCENDING:
            return SquatPhase.DESCENT
        if self.state == SquatState.BOTTOM:
            return SquatPhase.BOTTOM
        if self.state == SquatState.ASCENDING:
            return SquatPhase.ASCENT
        return None
    
    def get_squats(self):
        return self.squats
    
    def compute_times(self):
        results = []

        for i, squat in enumerate(self.squats):
            if not all(k in squat for k in ["start_time", "bottom_time", "end_time"]):
                continue
            
            descent = squat["bottom_time"] - squat["start_time"]
            ascent  = squat["end_time"] - squat["bottom_time"]
            total   = squat["end_time"] - squat["start_time"]

            results.append({
                "squat_id": squat["squat_id"],
                "descent_time": descent,
                "ascent_time": ascent,
                "total_time": total,
                "tempo_ratio": descent / ascent if ascent > 0 else None,
                "min_knee": squat["min_knee"],
                "max_trunk": squat["max_trunk"]
            })
    
        return results
    
    def normalize_squat_time(self):
        for squat in self.squats:
            start = squat["start_time"]
            end = squat["end_time"]
            total = end - start if end > start else None

            if not total:
                continue

            for frame in squat["frames"]:
                frame["phase_percent"] = (
                    (frame["time"] - start) / total
                ) * 100