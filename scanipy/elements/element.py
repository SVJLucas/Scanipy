import os

X_DIFF_TOLERANCE = 150


class Element:
    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step=None):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.pipeline_step = pipeline_step
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2

    def __lt__(self, other):
        return (self.x_min < other.x_min - X_DIFF_TOLERANCE) or \
            (abs(self.x_min - other.x_min) < X_DIFF_TOLERANCE and (self.y_min < other.y_min))
