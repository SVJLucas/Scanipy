from typing import Union
from PIL import Image
from fitz import Page
from scanipy.deeplearning.models import EquationToLatex
from .extractor import Extractor
from scanipy.elements import EquationElement

# Define the EquationExtractor class
class EquationExtractor(Extractor):
    """
    Represents an equation extractor for extracting equations from a document.

    Attributes:
        latex_ocr (str): Deep Learning Model to extract equations from images.
    """

    def __init__(self):
        """
        Initialize an EquationExtractor object.
        """
        # Initialize the OCR model for converting equation images to LaTeX
        self.latex_ocr = EquationToLatex()

    def extract(self, pdf_page: Page, page_image: Image.Image, equation_element: EquationElement) -> EquationElement:
        """
        Extracts an equation from a given page image based on the coordinates in the equation element.

        Args:
            page_image (PIL.Image): The page image from which to extract the equation.
            equation_element (EquationElement): The equation element containing the coordinates for extraction.

        Returns:
            EquationElement: The updated equation element with the extracted LaTeX content.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not isinstance(page_image, Image.Image):
            raise TypeError("page_image must be a PIL.Image object")
        if not isinstance(equation_element, EquationElement):
            raise TypeError("equation_element must be an EquationElement object")

        # Extract the coordinates from the equation element
        left = equation_element.x_min
        upper = equation_element.y_min
        right = equation_element.x_max
        lower = equation_element.y_max

        # Crop the image based on the coordinates
        equation_image = page_image.crop((left, upper, right, lower))

        # Convert the cropped equation image to LaTeX using the OCR model
        latex = self.latex_ocr(equation_image)

        # Update the equation element with the extracted LaTeX content
        equation_element.latex_content = latex

        return equation_element

    def __str__(self) -> str:
        """
        Returns a string representation of the EquationExtractor object.

        Returns:
            str: A string representation of the object.
        """
        return f"EquationExtractor(latex_ocr={self.latex_ocr})"
