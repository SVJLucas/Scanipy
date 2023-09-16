from typing import Union

# Define the Element class
class Element:
    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float,
                 pipeline_step:Union[int, None]=None, page_number: Union[int, None] = None,
                 intersection_percentage_threshold = 90):
        """
        Initialize an Element object with normalized coordinates, an optional pipeline step, and an intersection percentage threshold.

        Args:
            x_min (float): The minimum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_min (float): The minimum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            x_max (float): The maximum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_max (float): The maximum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            pipeline_step (Union[int, None], optional): The processing step in the pipeline to which this element belongs. Defaults to None.
            page_number (int): Specifies the page number on which the element is located.
            intersection_percentage_threshold (int, optional): The minimum percentage of intersection required for two elements to be considered overlapping. Defaults to 90 (%).

        Raises:
            ValueError:
                - If x_min >= x_max or y_min >= y_max.
                - If any coordinate is not in the range [0, 1].
            TypeError:
                - If the coordinates are not floats.
                - If pipeline_step is neither an integer nor None.
        """
        # Verify the input variable types
        if not isinstance(x_min, float) or not isinstance(y_min, float) or not isinstance(x_max, float) or not isinstance(y_max, float):
            raise TypeError("Coordinates must be floats")

        # Verify if coordinates are in the range 0 to 1
        if not (0 <= x_min <= 1 and 0 <= y_min <= 1 and 0 <= x_max <= 1 and 0 <= y_max <= 1):
            raise ValueError("Coordinates must be in the range from 0.0 to 1.0")

        # Verify if x_min is less than x_max and y_min is less than y_max
        if x_min >= x_max or y_min >= y_max:
            raise ValueError("Invalid coordinates: x_min should be less than x_max and y_min should be less than y_max")

        # Verify the pipeline_step type
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be an integer or None")
            
        # Verify the page_number type
        if pipeline_step is not None and not isinstance(page_number, int):
            raise TypeError("page_number must be an integer or None")

        # Initialize instance variables
        self._x_min = x_min
        self._y_min = y_min
        self._x_max = x_max
        self._y_max = y_max
        self._pipeline_step = pipeline_step
        self._page_number = page_number
        self._intersection_percentage_threshold = intersection_percentage_threshold

        # Calculate the center coordinates and width
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2
        self.width = x_max - x_min
        self.height = y_max - y_min

    def __repr__(self) -> str:
        """
        Provides a human-readable representation of the Element object.

        Returns:
            str: A string representation of the Element object.
        """
        return f"Element(x_min={self._x_min}, y_min={self._y_min}, x_max={self._x_max}, y_max={self._y_max}, pipeline_step={self._pipeline_step}, page_number={self._page_number})"

    def __str__(self) -> str:
        """
        Returns a string representation of the object, which is the same as its official representation.
        
        Returns:
            str: A string that can be used to recreate the object.
        """
        return self.__repr__()

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

        return self._column_before(other) or (self._same_column(other) and (self.y_min < other.y_min))

    def _column_before(self, other)->bool:
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

    def _same_column(self, other)->bool:
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
        return self._intersection_percentage(other) > self._intersection_percentage_threshold

    def _intersection_area(self, other)->int:
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

    def _intersection_percentage(self, other):
        """
        Calculate the percentage of intersection between this Element and another.

        Args:
            other (Element): Another Element object.

        Returns:
            float: The percentage of intersection.
        """
        if not isinstance(other, Element):
            raise TypeError("other must be an instance or subclass of Element")

        intersection_area = self._intersection_area(other)
        self_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)

        return intersection_area / self_area * 100

    @property
    def x_min(self) -> float:
        """
        Gets the minimum x-coordinate of the element.

        Returns:
            float: The minimum x-coordinate, normalized to the image width.
        """
        return self._x_min

    @x_min.setter
    def x_min(self, x_min: float):
        """
        Sets the minimum x-coordinate of the element.

        Args:
            x_min (float): The new minimum x-coordinate, normalized to the image width (range: 0 to 1).

        Raises:
            ValueError: If x_min is not in the range [0, 1].
            TypeError: If x_min is not a float.
        """
        if not isinstance(x_min, float):
            raise TypeError("x_min must be a float.")
        if not 0 <= x_min <= 1:
            raise ValueError("x_min must be in the range [0, 1].")
        self._x_min = x_min

    @property
    def y_min(self) -> float:
        """
        Gets the minimum y-coordinate of the element.

        Returns:
            float: The minimum y-coordinate, normalized to the image height.
        """
        return self._y_min

    @y_min.setter
    def y_min(self, y_min: float):
        """
        Sets the minimum y-coordinate of the element.

        Args:
            y_min (float): The new minimum y-coordinate, normalized to the image height (range: 0 to 1).

        Raises:
            ValueError: If y_min is not in the range [0, 1].
            TypeError: If y_min is not a float.
        """
        if not isinstance(y_min, float):
            raise TypeError("y_min must be a float.")
        if not 0 <= y_min <= 1:
            raise ValueError("y_min must be in the range [0, 1].")
        self._y_min = y_min

    @property
    def x_max(self) -> float:
        """
        Gets the maximum x-coordinate of the element.

        Returns:
            float: The maximum x-coordinate, normalized to the image width.
        """
        return self._x_max

    @x_max.setter
    def x_max(self, x_max: float):
        """
        Sets the maximum x-coordinate of the element.

        Args:
            x_max (float): The new maximum x-coordinate, normalized to the image width (range: 0 to 1).

        Raises:
            ValueError: If x_max is not in the range [0, 1].
            TypeError: If x_max is not a float.
        """
        if not isinstance(x_max, float):
            raise TypeError("x_max must be a float.")
        if not 0 <= x_max <= 1:
            raise ValueError("x_max must be in the range [0, 1].")
        self._x_max = x_max

    @property
    def y_max(self) -> float:
        """
        Gets the maximum y-coordinate of the element.

        Returns:
            float: The maximum y-coordinate, normalized to the image height.
        """
        return self._y_max

    @y_max.setter
    def y_max(self, y_max: float):
        """
        Sets the maximum y-coordinate of the element.

        Args:
            y_max (float): The new maximum y-coordinate, normalized to the image height (range: 0 to 1).

        Raises:
            ValueError: If y_max is not in the range [0, 1].
            TypeError: If y_max is not a float.
        """
        if not isinstance(y_max, float):
            raise TypeError("y_max must be a float.")
        if not 0 <= y_max <= 1:
            raise ValueError("y_max must be in the range [0, 1].")
        self._y_max = y_max
    @property
    def pipeline_step(self) -> Union[int, None]:
        """
        Gets the pipeline step associated with the element.

        Returns:
            Union[int, None]: The pipeline step, which can be an integer or None.
        """
        return self._pipeline_step

    @pipeline_step.setter
    def pipeline_step(self, pipeline_step: Union[int, None]):
        """
        Sets the pipeline step associated with the element.

        Args:
            pipeline_step (Union[int, None]): The new pipeline step, which can be an integer or None.

        Raises:
            TypeError: If pipeline_step is neither an integer nor None.
        """
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be either an integer or None.")
        self._pipeline_step = pipeline_step

    @property
    def page_number(self) -> Union[int, None]:
        """
        Gets the page number associated with the element.

        Returns:
            Union[int, None]: The page number, which can be an integer or None.
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number: Union[int, None]):
        """
        Sets the page number associated with the element.

        Args:
            page_number (Union[int, None]): The new page number, which can be an integer or None.

        Raises:
            TypeError: If page_number is neither an integer nor None.
        """
        if page_number is not None and not isinstance(page_number, int):
            raise TypeError("pipeline_step must be either an integer or None.")
        self._page_number = page_number
