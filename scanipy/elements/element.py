import os

X_DIFF_TOLERANCE = 150
INTERSECTION_PERCENTAGE_THRESHOLD = 90

class Element:
    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step=None):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.pipeline_step = pipeline_step
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2
        self.width = x_max - x_min

    def __lt__(self, other):
        return self.column_before(other) or (self.same_column(other) and (self.y_min < other.y_min))

    def column_before(self, other):
        max_width = max(self.width, other.width)
        return self.x_min < other.x_min - max_width / 2

    def same_column(self, other):
        max_width = max(self.width, other.width)
        return abs(self.x_min - other.x_min) < max_width / 2

    def is_in(self, other):
        return self.intersection_percentage(other) > INTERSECTION_PERCENTAGE_THRESHOLD

    def intersection_area(self, other):
        """Calculates the area of intersection of two rectangles.

        Args:
          self: The first rectangle.
          other: The second rectangle.

        Returns:
          The area of intersection of the two rectangles.
        """
        x_min = max(self.x_min, other.x_min)
        x_max = min(self.x_max, other.x_max)
        y_min = max(self.y_min, other.y_min)
        y_max = min(self.y_max, other.y_max)

        if x_max < x_min or y_max < y_min:
            return 0

        return (x_max - x_min) * (y_max - y_min)

    def intersection_percentage(self, other):
        """Calculates the percentage of intersection of the areas of two rectangles.

        Args:
          self: The first rectangle.
          other: The second rectangle.

        Returns:
          The percentage of intersection of the two rectangles, as a float between 0
          and 1.
        """
        intersection_area = self.intersection_area(other)
        self_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)

        return intersection_area / self_area * 100
