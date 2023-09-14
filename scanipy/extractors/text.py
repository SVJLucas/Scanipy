from typing import Union
from PIL import Image
from pdfplumber.page import Page
from .extractors import Extractor
from .elements import TextElement 
from deeplearning.models import TextOCR 

# Define the TextExtractor class
class TextExtractor(Extractor):
    """
    Represents a text extractor for extracting text from a document.
    """

    def __init__(self, use_ocr: bool, lang: str = 'eng):
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
        self.text_ocr = TextOCR(lang)

    def process_text_image(self, text_element: TextElement, text_image: Image, pdf_page: Page) -> str:
        """
        Process the text image based on OCR settings and equation presence.

        Args:
            text_element (TextElement): The text element containing the coordinates for extraction.
            text_image (Image): The cropped text image.
            pdf_page (Page): The PDF page containing the text element.

        Returns:
            str: The extracted text content.
        """
        # Use OCR or not based on the use_ocr flag and whether the text element contains equations
        if self.use_ocr:
            if text_element.has_equation_inside:
                return self.text_ocr.get_text_and_equations_with_ocr(text_image)
            else:
                return self.text_ocr.get_text_with_ocr(text_image)
        else:
            if text_element.has_equation_inside:
                return self.text_ocr.get_text_and_equations_without_ocr(text_image, pdf_page)
            else:
                return self.text_ocr.get_text_without_ocr(text_image, pdf_page)

    def extract(self, pdf_page: Page, page_image: Image, text_element: TextElement, page) -> TextElement:
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
        if not isinstance(page_image, Image):
            raise TypeError("page_image must be a PIL.Image object")
        if not isinstance(text_element, TextElement):
            raise TypeError("text_element must be a TextElement object")

        # Extract the coordinates from the text element
        left = text_element.x_min
        upper = text_element.y_min
        right = text_element.x_max
        lower = text_element.y_max

        # Crop the image based on the coordinates
        text_image = page_image.crop((left, upper, right, lower))

        # Process the cropped text image and extract the text content
        text_content = self.process_text_image(text_element, text_image, pdf_page)

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
