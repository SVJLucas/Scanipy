import random
import string
from typing import Union
from PIL import Image
from .extractors import Extractor
from .elements import ImageElement

# Define the ImageExtractor class
class ImageExtractor(Extractor):
    """
    Represents an image extractor for extracting images from a document.

    Attributes:
        unique_keys (set): A set to store unique keys for each extracted image.
    """

    def __init__(self):
        """
        Initialize an ImageExtractor object.
        """
        # Initialize a set to store unique keys for each extracted image
        self.unique_keys = set()

    def generate_random_string(self, length: int = 32) -> str:
        """
        Generate a random string of a given length consisting of characters a-z, A-Z, and 0-9.

        Args:
            length (int): The length of the random string to be generated. Default is 32.

        Returns:
            str: The generated random string.
        """
        # Verify the input variable type
        if not isinstance(length, int):
            raise TypeError("length must be an integer")

        # Define the characters that can be used in the random string
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9

        # Generate the random string using random.choices()
        random_string = ''.join(random.choices(characters, k=length))

        return random_string

    def extract(self, page_image: Image, image_element: ImageElement, unique_key: Union[str, None] = None, image_extension: str = 'png' ) -> ImageElement:
        """
        Extracts an image from a given page image based on the coordinates in the image element.

        Args:
            page_image (PIL.Image): The page image from which to extract the image.
            image_element (ImageElement): The image element containing the coordinates for extraction.
            unique_key (Union[str, None], optional): A unique key for the image. If None, a random unique key will be generated.
            image_extension (str): The extension of the image. Defauls to be 'png'.

        Returns:
            ImageElement: The updated image element with the extracted image content.

        Raises:
            TypeError: If the unique_key is not unique.
        """

        # Verify the input variable types
        if not isinstance(page_image, Image):
            raise TypeError("page_image must be a PIL.Image object")
        if not isinstance(image_element, ImageElement):
            raise TypeError("image_element must be an ImageElement object")
        if not isinstance(unique_key, str) and unique_key is not None:
            raise TypeError("unique_key must be an string or None")
        if not isinstance(image_extension, str) and image_extension is not None:
            raise TypeError("image_extension must be an string or None")
        
        # Extract the coordinates from the image element
        left = image_element.x_min
        upper = image_element.y_min
        right = image_element.x_max
        lower = image_element.y_max

        # Crop the image based on the coordinates
        image_content = page_image.crop((left, upper, right, lower))

        # Generate a unique key if not provided
        if unique_key is None:
            unique_key = self.generate_random_string()
            while unique_key in self.unique_keys:
                unique_key = self.generate_random_string()
        elif unique_key in self.unique_keys:
            raise TypeError("The parameters unique_key must be unique.")

        # Update the set of used keys
        self.unique_keys.add(unique_key)

        # Update the image element with the extracted image content and unique key
        image_element.image_content = image_content
        image_element.unique_key = unique_key
        image_element.image_extension  = image_extension

        return image_element

    def __str__(self) -> str:
        """
        Returns a string representation of the ImageExtractor object.

        Returns:
            str: A string representation of the object.
        """
        return f"ImageExtractor(unique_keys={self.unique_keys})"
