

class SquatEvaluator:
    def __init__(self):
        self.MIN_KNEE_DEPTH = 110
        self.MAX_TRUNK_ANGLE = 45
        self.TEMPO_RANGE = (0.5, 1.2)

    def evaluate(self, squat):
        errors = []

        # 1️⃣ Głębokość
        if squat["min_knee"] > self.MIN_KNEE_DEPTH:
            errors.append("Zbyt płytki przysiad")        
        
        # 2️⃣ Tułów
        if squat["max_trunk"] > self.MAX_TRUNK_ANGLE:
            errors.append("Zbyt duże pochylenie tułowia")

        # 3️⃣ Tempo
        descent = squat["bottom_frame"] - squat["start_frame"]
        ascent  = squat["end_frame"] - squat["bottom_frame"]

        ratio = descent / ascent if ascent > 0 else None
        if ratio is None or not self.TEMPO_RANGE[0] <= ratio <= self.TEMPO_RANGE[1]:
            errors.append("Nieprawidłowe tempo ruchu")

        squat["tempo_ratio"] = ratio
        squat["valid"] = len(errors) == 0
        squat["errors"] = errors

        return squat