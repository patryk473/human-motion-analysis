from src.pose import SquatState

class RealTimeFeedback:
    def __init__(self):
        self.MAX_TRUNK = 45
        self.MIN_KNEE_DEPTH = 100

    def evaluate(self, knee, trunk, state):
        messages = []

        if state in (SquatState.DESCENDING, SquatState.BOTTOM):
            if trunk > self.MAX_TRUNK:
                messages.append("Za duze pochylenie tulowia")

        if state == SquatState.DESCENDING:
            if knee > self.MIN_KNEE_DEPTH:
                    messages.append("Zejdz nizej")
            if knee < self.MIN_KNEE_DEPTH:
                    messages.append("Poprawna glebokosc")

        if state == SquatState.BOTTOM:
            messages.append("Poprawna glebokosc")

        return messages