from typing import Union
from .element import Element

# Define the TitleElement class
class TitleElement(Element):
    """
    Represents a title element within a document.

    Attributes:
        title_content (str): The content of the title element.
    """

    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, 
                 pipeline_step: Union[int, None] = None):
        """
        Initialize a TitleElement object.

        Args:
            x_min (int): The minimum x-coordinate.
            y_min (int): The minimum y-coordinate.
            x_max (int): The maximum x-coordinate.
            y_max (int): The maximum y-coordinate.
            pipeline_step (Union[int, None], optional): The pipeline step, can be None.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not all(isinstance(var, int) for var in [x_min, y_min, x_max, y_max]):
            raise TypeError("Coordinates must be integers")
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be an integer or None")

        # Initialize instance variables by calling the parent class constructor
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)

        # Initialize additional instance variable specific to TitleElement
        self._title_content = None

    # Setter and Getter for title_content
    @property
    def title_content(self) -> Union[str, None]:
        """
        Gets the content of the title element.

        Returns:
            Union[str, None]: The content of the title element.
        """
        return self._title_content

    @title_content.setter
    def title_content(self, value: Union[str, None]):
        """
        Sets the content of the title element.

        Args:
            value (Union[str, None]): The new content for the title element.

        Raises:
            TypeError: If the provided value is not a string or None.
        """
        if value is not None and not isinstance(value, str):
            raise TypeError("title_content must be a string or None")
        self._title_content = value

    def __str__(self) -> str:
        """
        Returns a string representation of the TitleElement object.

        Returns:
            str: A string representation of the object.
        """
        return f"TitleElement(x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, title_content={self.title_content})"

    def generate_markdown(self, output_directory: str) -> str:
        """
        Generate the Markdown representation of the title element.

        Args:
            output_directory (str): The directory where the text file will be saved.

        Returns:
            str: Markdown representation of the title element.
        """
        # Add Markdown header formatting to the title content
        formatted_title = '## ' + self.title_content + '\n\n'
        return formatted_title
