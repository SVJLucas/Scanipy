import os
from .element import Element
from typing import Union, Any
import matplotlib.pyplot as plt

# Define the ImageElement class, which inherits from the Element class
class ImageElement(Element):
    """
    Represents an image element within a document.

    Attributes:
        unique_key (str): A unique identifier for the image element.
        image_content (Any): The actual content of the image.
        image_extension (str): The file extension for the image (e.g., 'jpg', 'png').
    """

    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, pipeline_step: Union[int, None] = None):
        """
        Initialize an ImageElement object.

        Args:
            x_min (int): The minimum x-coordinate.
            y_min (int): The minimum y-coordinate.
            x_max (int): The maximum x-coordinate.
            y_max (int): The maximum y-coordinate.
            pipeline_step (Union[int, None], optional): The pipeline step, can be None.

        Raises:
            ValueError: If x_min >= x_max or y_min >= y_max.
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not all(isinstance(var, int) for var in [x_min, y_min, x_max, y_max]):
            raise TypeError("Coordinates must be integers")
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be an integer or None")

        # Initialize instance variables by calling the parent class constructor
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)

        # Initialize additional instance variables specific to ImageElement
        self.unique_key = None
        self.image_content = None
        self.image_extension = None

    @property
    def unique_key(self) -> str:
        """
        Gets the unique key of the image element.

        Returns:
            str: The unique key of the image element.
        """
        return self._unique_key

    @unique_key.setter
    def unique_key(self, value: str):
        """
        Sets the unique key of the image element.

        Args:
            value (str): The new unique key.

        Raises:
            TypeError: If the provided value is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("unique_key must be a string")
        self._unique_key = value

    @property
    def image_content(self) -> Any:
        """
        Gets the content of the image element.

        Returns:
            Any: The content of the image element.
        """
        return self._image_content

    @image_content.setter
    def image_content(self, value: Any):
        """
        Sets the content of the image element.

        Args:
            value (Any): The new content for the image element.
        """
        # Type verification can be more specific depending on what 'Any' encompasses
        self._image_content = value

    @property
    def image_extension(self) -> str:
        """
        Gets the file extension of the image element.

        Returns:
            str: The file extension of the image element.
        """
        return self._image_extension

    @image_extension.setter
    def image_extension(self, value: str):
        """
        Sets the file extension of the image element.

        Args:
            value (str): The new file extension for the image element.

        Raises:
            TypeError: If the provided value is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("image_extension must be a string")
        self._image_extension = value

    def __str__(self) -> str:
        """
        Returns a string representation of the ImageElement object.
    
        Returns:
            str: A string representation of the object.
        """
        return f"ImageElement(unique_key={self.unique_key}, x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, image_extension={self.image_extension})"

    def display_image(self):
        """
        Display the image content using Matplotlib.

        Raises:
            ValueError: If image_content is None or not properly set.
        """
        if self.image_content is None:
            raise ValueError("image_content is not set")

        # Assuming image_content has format compatible with imshow
        plt.imshow(self.image_content)
        plt.title(f"Image: {self.unique_key}")
        plt.axis('off')  # Turn off axis numbers and ticks
        plt.show()

    def generate_markdown(self, output_directory) -> str:
        """
        Generate the Markdown representation of the image element and save the image to a file.

        Args:
            output_directory (str): The directory where the image file will be saved.

        Returns:
            str: Markdown representation of the image element.
        """
        # Create the filename for the image
        filename = f"{self.unique_key}.{self.image_extension}"

        # Create the full path where the image will be saved
        output_path = os.path.join(output_directory, filename)

        # Save the image content to the file
        self.image_content.save(open(output_path, "wb"))

        # Return the Markdown representation of the image
        return f"\n![image]({filename})\n\n"

