import numpy as np
from collections import deque

class MovingAverage:
    def __init__(self, window=5):
        self.buffer = deque(maxlen=window)

    def update(self, value):
        self.buffer.append(value)
        return np.mean(self.buffer)