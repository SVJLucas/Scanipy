import easyocr
import pytesseract
import numpy as np
from PIL import Image
from typing import Union

class TextOCR:
    def __init__(self, lang: str, device: str):
        """
        Initialize the TextOCR object.

        Args:
            lang (str): The language for OCR.
            device (str): The device to use for OCR ('cpu' or other).

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not isinstance(lang, str):
            raise TypeError("lang must be a string")
        if not isinstance(device, str):
            raise TypeError("device must be a string")

        # Initialize instance variables
        self.device = device
        if device == 'cpu':
            if lang != 'en':
                self.lang = 'en+' + lang
            else:
                self.lang = 'en'
            self.model = pytesseract.image_to_string
        else:
            self.lang = lang
            if self.lang != 'en':
                self.model = easyocr.Reader([self.lang, 'en']).readtext
            else:
                self.model = easyocr.Reader(['en']).readtext

    def __call__(self, image: Image.Image) -> str:
        """
        Perform OCR on the given image.

        Args:
            image (Image): The image to perform OCR on.

        Returns:
            str: The extracted text.
        """
        # Verify the input image type
        if not isinstance(image, Image.Image):
            raise TypeError("image must be a PIL.Image object")

        # Perform OCR based on the device
        if self.device == 'cpu':
            if self.lang == 'en':
                text = self.model(image)
            else:
                text = self.model(image, lang=self.lang) # type: ignore
        else:
            np_image = np.array(image)
            detections = self.model.recognize(np_image)
            text = ' '.join(detection[1] for detection in detections)

        # Remove newline characters from the extracted text
        text = text.replace('\n', '')

        return text

    def __repr__(self) -> str:
        """
        Returns a official string representation of the TextOCR object.

        Returns:
            str: A string representation of the object.
        """
        return f"TextOCR(lang={self.lang}, device={self.device})"

    def __str__(self) -> str:
        """
        Returns a string representation of the TextOCR object, which is the same as its official representation.
        
        Returns:
            str: A string that can be used to recreate the EquationToLatex object.
        """
        return self.__repr__()
