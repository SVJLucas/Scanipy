from typing import Union

# Define the Element class
class Element:
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int,
                 pipeline_step:Union[int, None]=None, intersection_percentage_threshold = 90):
        """
        Initialize an Element object with coordinates, an optional pipeline step, and an intersection percentage threshold.
    
        Args:
            x_min (int): The minimum x-coordinate of the element.
            y_min (int): The minimum y-coordinate of the element.
            x_max (int): The maximum x-coordinate of the element.
            y_max (int): The maximum y-coordinate of the element.
            pipeline_step (Union[int, None], optional): The pipeline step associated with the element. Defaults to None.
            intersection_percentage_threshold (int, optional): The threshold for intersection percentage. Defaults to 90.
    
        Raises:
            ValueError: If x_min >= x_max or y_min >= y_max.
            TypeError: If the types of the arguments do not match the expected types.
        """
        # Verify the input variable types #TODO
        # if not all(isinstance(var, int) for var in [x_min, y_min, x_max, y_max]):
        #     raise TypeError("Coordinates must be integers")
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be an integer or None")

        # Verify the input variable values
        if x_min >= x_max:
            raise ValueError("x_min should be less than x_max")
        if y_min >= y_max:
            raise ValueError("y_min should be less than y_max")

        # Initialize instance variables
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.pipeline_step = pipeline_step
        self.intersection_percentage_threshold = intersection_percentage_threshold

        # Calculate the center coordinates and width
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2
        self.width = x_max - x_min

    def __lt__(self, other)->bool:
        """
        Less than operator for Element objects.

        Args:
            other (Element): Another Element object.

        Returns:
            bool: True if this Element is "less than" the other, False otherwise.

        Raises:
            TypeError: If 'other' is not an instance or subclass of Element.
        """
        
        if not isinstance(other, Element):
            raise TypeError("other must be an instance or subclass of Element")

        return self.column_before(other) or (self.same_column(other) and (self.y_min < other.y_min))
        
    def column_before(self, other)->bool:
        """
        Check if this Element is in a column before the other Element.

        Args:
            other (Element): Another Element object.

        Returns:
            bool: True if in a column before, False otherwise.
        """
        
        if not isinstance(other, Element):
            raise TypeError("other must be an instance or subclass of Element")
            
        max_width = max(self.width, other.width)
        return self.x_min < other.x_min - max_width / 2

    def same_column(self, other)->bool:
        """
        Check if this Element is in the same column as the other Element.

        Args:
            other (Element): Another Element object.

        Returns:
            bool: True if in the same column, False otherwise.
        """
        
        if not isinstance(other, Element):
            raise TypeError("other must be an instance or subclass of Element")
        
        max_width = max(self.width, other.width)
        return abs(self.x_min - other.x_min) < max_width / 2

    def is_in(self, other)->bool:
        """
        Check if this Element is inside the other Element.

        Args:
            other (Element): Another Element object.

        Returns:
            bool: True if inside, False otherwise.
        """
        if not isinstance(other, Element):
            raise TypeError("other must be an instance or subclass of Element")
        return self.intersection_percentage(other) > self.intersection_percentage_threshold

    def intersection_area(self, other)->int:
        """
        Calculate the area of intersection between this Element and another.

        Args:
            other (Element): Another Element object.

        Returns:
            int: The area of intersection.
        """

        if not isinstance(other, Element):
            raise TypeError("other must be an instance or subclass of Element")
        
        x_min = max(self.x_min, other.x_min)
        x_max = min(self.x_max, other.x_max)
        y_min = max(self.y_min, other.y_min)
        y_max = min(self.y_max, other.y_max)

        if x_max < x_min or y_max < y_min:
            return 0

        return (x_max - x_min) * (y_max - y_min)

    def intersection_percentage(self, other):
        """
        Calculate the percentage of intersection between this Element and another.

        Args:
            other (Element): Another Element object.

        Returns:
            float: The percentage of intersection.
        """
        if not isinstance(other, Element):
            raise TypeError("other must be an instance or subclass of Element")
            
        intersection_area = self.intersection_area(other)
        self_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)

        return intersection_area / self_area * 100
