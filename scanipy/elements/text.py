from typing import Union
from .element import Element

# Define the TextElement class, which inherits from the Element class
class TextElement(Element):
    """
    Represents a text element within a document.

    Attributes:
        text_content (str): The content of the text element.
    """

    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, pipeline_step: Union[int, None] = None, content: Union[str, None] = None):
        """
        Initialize a TextElement object.

        Args:
            x_min (int): The minimum x-coordinate.
            y_min (int): The minimum y-coordinate.
            x_max (int): The maximum x-coordinate.
            y_max (int): The maximum y-coordinate.
            pipeline_step (Union[int, None], optional): The pipeline step, can be None.
            content (Union[str, None], optional): The content of the text element.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not all(isinstance(var, int) for var in [x_min, y_min, x_max, y_max]):
            raise TypeError("Coordinates must be integers")
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be an integer or None")
        if content is not None and not isinstance(content, str):
            raise TypeError("content must be a string or None")

        # Initialize instance variables by calling the parent class constructor
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)

        # Initialize additional instance variable specific to TextElement
        self._text_content = content

    # Setter and Getter for text_content
    @property
    def text_content(self) -> Union[str, None]:
        """
        Gets the content of the text element.

        Returns:
            Union[str, None]: The content of the text element.
        """
        return self._text_content

    @text_content.setter
    def text_content(self, value: Union[str, None]):
        """
        Sets the content of the text element.

        Args:
            value (Union[str, None]): The new content for the text element.

        Raises:
            TypeError: If the provided value is not a string or None.
        """
        if value is not None and not isinstance(value, str):
            raise TypeError("text_content must be a string or None")
        self._text_content = value

    def __str__(self) -> str:
        """
        Returns a string representation of the TextElement object.

        Returns:
            str: A string representation of the object.
        """
        return f"TextElement(x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, text_content={self.text_content})"

    def generate_markdown(self, output_directory: str) -> str:
        """
        Generate the Markdown representation of the text element.

        Args:
            output_directory (str): The directory where the text file will be saved.

        Returns:
            str: Markdown representation of the text element.
        """
        # Concatenate the text content with newlines for Markdown formatting
        formatted_text = self.text_content + '\n\n'
        return formatted_text
