from typing import Union
from PIL import Image
from pdfplumber.page import Page
from .extractor import Extractor
from scanipy.elements import TextElement, TitleElement
import numpy as np
import cv2
from scanipy.deeplearning.models import TextOCR

# Define the TextExtractor class
class TextExtractor(Extractor):
    """
    Represents a text extractor for extracting text from a document.
    """

    def __init__(self, use_ocr: bool = False, lang: str = 'eng'):
        """
        Initialize a TextExtractor object.

        Args:
            use_ocr (bool): Whether to use OCR for text extraction or not.
            lang (str): The language of the text. Defaults to english.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not isinstance(use_ocr, bool):
            raise TypeError("use_ocr must be a boolean")

        # Initialize OCR settings and OCR model
        self.use_ocr = use_ocr
        self.text_ocr = TextOCR(lang, use_ocr=use_ocr) #TODO

    def process_text_image(self, text_image: Image, pdf_page: Page, dimensions: tuple, fitz_factor: float) -> str:
        """
        Process the text image based on OCR settings and equation presence.

        Args:
            text_element (TextElement): The text element containing the coordinates for extraction.
            text_image (Image): The cropped text image.
            pdf_page (Page): The PDF page containing the text element.

        Returns:
            str: The extracted text content.
        """
        return self.text_ocr(pdf_page, text_image, dimensions, fitz_factor)
        # Use OCR or not based on the use_ocr flag and whether the text element contains equations
        if self.use_ocr:
            if text_element.has_equation_inside:
                return self.text_ocr.get_text_and_equations_with_ocr(text_element, text_image)
            else:
                return self.text_ocr.get_text_with_ocr(text_element, text_image)
        else:
            if text_element.has_equation_inside:
                return self.text_ocr.get_text_and_equations_without_ocr(text_element, text_image, pdf_page)
            else:
                return self.text_ocr.get_text_without_ocr(text_element, text_image, pdf_page)

    def extract(self, pdf_page: Page, page_image: Image.Image, text_element: TextElement) -> TextElement:
        """
        Extracts text from a given page image based on the coordinates in the text element.

        Args:
            pdf_page (Page): The PDF page from which to extract the text.
            page_image (Image): The page image from which to extract the text.
            text_element (TextElement): The text element containing the coordinates for extraction.
            page: Additional page context (not used in this example).

        Returns:
            TextElement: The updated text element with the extracted text content.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not isinstance(page_image, Image.Image):
            raise TypeError("page_image must be a PIL.Image object")
        if not isinstance(text_element, Union[TextElement, TitleElement]):
            raise TypeError("text_element must be a TextElement or TitleElement object")

        # Extract the coordinates from the text element
        left = text_element.x_min
        upper = text_element.y_min
        right = text_element.x_max
        lower = text_element.y_max
        dimensions = left, upper, right, lower

        fitz_factor = pdf_page.rect.width/page_image.size[0]

        # Crop the image based on the coordinates
        text_image = page_image.crop(dimensions)

        # Process the cropped text image and extract the text content
        text_content = self.process_text_image(text_image, pdf_page, dimensions, fitz_factor)

        # Update the text element with the extracted text content
        text_element.text_content = text_content

        return text_element

    def __str__(self) -> str:
        """
        Returns a string representation of the TextExtractor object.

        Returns:
            str: A string representation of the object.
        """
        return f"TextExtractor(use_ocr={self.use_ocr}, text_ocr={self.text_ocr})"
