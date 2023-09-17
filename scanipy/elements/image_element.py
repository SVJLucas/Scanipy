import os
import logging
from .element import Element
from .equation_element import EquationElement
from typing import Union, Any, List
import matplotlib.pyplot as plt

# Define the ImageElement class, which inherits from the Element class
class ImageElement(Element):
    """
    Represents an image element within a document.

    Attributes:
        unique_key (str): A unique identifier for the image element.
        image_content (Any): The actual content of the image.
        image_extension (str): The file extension for the image (e.g., 'jpg', 'png').
        has_equation_inside (bool): If there's some equation inside the image.
        equations_inside (List['EquationElement']): The equations elements that are inside the image
    """

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float,
                 pipeline_step: Union[int, None] = None, page_number: Union[int, None] = None):
        """
        Initialize an ImageElement object.

        Args:
            x_min (float): The minimum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_min (float): The minimum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            x_max (float): The maximum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_max (float): The maximum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            pipeline_step (Union[int, None], optional): The pipeline step, can be None.
            page_number (int): Specifies the page number on which the element is located.

        Raises:
            ValueError: If x_min >= x_max or y_min >= y_max.
            TypeError: If the types of the arguments are not as expected.
        """

        # Initialize instance variables by calling the parent class constructor
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step, page_number)

        # Initialize additional instance variables specific to ImageElement
        self._unique_key = None
        self._image_content = None
        self._image_extension = None
        self._equations_inside = []

    @property
    def equations_inside(self) -> List['EquationElement']:
        """
        Get the equations inside the element.

        Returns:
            List[EquationElement]: List of EquationElement contained in the element.
        """
        # Return the equation elements stored in the private variable
        return self._equations_inside

    @equations_inside.setter
    def equations_inside(self, value: List['EquationElement']) -> None:
        """
        Sets the equations inside the element.

        Args:
            value (List[EquationElement]): The new list of EquationElement values.

        Raises:
            TypeError: If the provided value is not a list of EquationElement.
        """
        # Check if the provided value is a list of EquationElement
        if not all(isinstance(v, EquationElement) for v in value):  # Replace 'EquationElement' with the actual class name if needed
            raise TypeError("equations_inside must be a list of EquationElement")
        
        # Set the equation elements in the private variable
        self._equations_inside = value

    @property
    def has_equation_inside(self) -> bool:
        """
        Determines if the element contains equations.
    
        This method checks if the element has any equations inside it and returns a boolean value accordingly.
    
        Returns:
            bool: True if the element contains equations, otherwise False.
        """
        return self._has_equation_inside

    @has_equation_inside.setter
    def has_equation_inside(self, value: bool):
        """
        Sets a boolean that checks if the element has any equations inside it.

        Args:
            value (bool): The new boolean value.

        Raises:
            TypeError: If the provided value is not a bool.
        """
        if not isinstance(value, bool):
            raise TypeError("has_equation_inside must be a bool")
        self._has_equation_inside = value

    @property
    def unique_key(self) -> str | None:
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
    def image_extension(self) -> str | None:
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

    def __repr__(self) -> str:
        """
        Returns a string representation of the ImageElement object.
    
        Returns:
            str: A string representation of the object.
        """
        return f"ImageElement(unique_key={self.unique_key}, x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, image_extension={self.image_extension}, has_equation_inside={self.has_equation_inside}, equations_inside={self.equations_inside})"

    def __str__(self):
        """
        Returns a string representation of the object, which is the same as its official representation.
        
        Returns:
            str: A string that can be used to recreate the object.
        """
        return self.__repr__()
        
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

    def generate_markdown(self, output_directory: str) -> str:
        """
        Generate the Markdown representation of the image element and save the image to a file.

        Args:
            output_directory (str): The directory where the image file will be saved.

        Returns:
            str: Markdown representation of the image element.
        """
        # If the image is an equation, don't print it
        if self.has_equation_inside:
            return '\n'


        if self.image_content == None:
            logging.warning('Tried to write a NoneType object')
            return '\n\n'
        
        # Create the filename for the image
        filename = f"{self.unique_key}.{self.image_extension}"

        # Create the full path where the image will be saved
        output_path = os.path.join(output_directory, filename)

        # Save the image content to the file
        self.image_content.save(open(output_path, "wb"))

        # Return the Markdown representation of the image
        return f"\n![image]({filename})\n\n"

