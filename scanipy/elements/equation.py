from typing import Union
from .element import Element

# Define the EquationElement class
class EquationElement(Element):
    """
    Represents an equation element within a document.

    Attributes:
        latex_content (Union[str, None]): The LaTeX content of the equation element.
        is_inside_text (bool): Flag indicating if the equation is part of a text block.
    """

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, 
                 pipeline_step: Union[int, None] = None, page_number: Union[int, None] = None):
        """
        Initialize an EquationElement object.

        Args:
            x_min (float): The minimum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_min (float): The minimum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            x_max (float): The maximum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_max (float): The maximum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            pipeline_step (Union[int, None], optional): The pipeline step, can be None.
            page_number (int): Specifies the page number on which the element is located.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be an integer or None")

        # Initialize instance variables by calling the parent class constructor
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step, page_number)

        # Initialize additional instance variables specific to EquationElement
        self._latex_content = None
        self._is_inside_text = False

    # Setter and Getter for latex_content
    @property
    def latex_content(self) -> Union[str, None]:
        """
        Gets the LaTeX content of the equation element.

        Returns:
            Union[str, None]: The LaTeX content of the equation element.
        """
        return self._latex_content

    @latex_content.setter
    def latex_content(self, value: Union[str, None]):
        """
        Sets the LaTeX content of the equation element.

        Args:
            value (Union[str, None]): The new LaTeX content for the equation element.

        Raises:
            TypeError: If the provided value is not a string or None.
        """
        if value is not None and not isinstance(value, str):
            raise TypeError("latex_content must be a string or None")
        self._latex_content = value

    # Setter and Getter for is_inside_text
    @property
    def is_inside_text(self) -> bool:
        """
        Gets the flag indicating if the equation is part of a text block.

        Returns:
            bool: True if the equation is part of a text block, False otherwise.
        """
        return self._is_inside_text

    @is_inside_text.setter
    def is_inside_text(self, value: bool):
        """
        Sets the flag indicating if the equation is part of a text block.

        Args:
            value (bool): The new flag value.

        Raises:
            TypeError: If the provided value is not a boolean.
        """
        if not isinstance(value, bool):
            raise TypeError("is_inside_text must be a boolean")
        self._is_inside_text = value

    def __str__(self) -> str:
        """
        Returns a string representation of the EquationElement object.

        Returns:
            str: A string representation of the object.
        """
        return f"EquationElement(x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, latex_content={self.latex_content}, is_inside_text={self.is_inside_text})"

    def generate_markdown(self, output_directory: str) -> str:
        """
        Generate the Markdown representation of the equation element.

        Args:
            output_directory (str): The directory where the equation will be saved.

        Returns:
            str: Markdown representation of the equation element.
        """
        # Concatenate the LaTeX content with newlines for Markdown formatting
        formatted_equation = self.latex_content + '\n\n'
        return formatted_equation
