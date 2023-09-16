import torch
import pix2text
from PIL import Image
from pdfplumber.page import Page
from .extractor import Extractor
from scanipy.elements import TextElement 
from typing import Union, Tuple, List, Dict


class TextExtractor:
  def __init__(self, lang: str, tolerance: float = 1.5):
    """
    Initialize a TextExtractor object.

    Args:
        lang (str): The language for OCR.
        tolerance (float): The tolerance level for text extraction. Default is 1.5.

    """
    # Check if CUDA is available and set the device accordingly
    self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Initialize OCR model for text and equations
    self.text_equations_ocr = pix2text.Pix2Text(device=self.device)

    # Set the language for OCR
    self.lang = lang

    # Initialize the TextOCR object
    self.text_ocr = TextOCR(self.lang, self.device)

    # Set the tolerance level for text extraction
    self.tolerance = tolerance

  @property
  def tolerance(self) -> float:
    """
    Getter for the 'tolerance' attribute.

    Returns:
        float: The current tolerance level for text extraction.
    """
    return self._tolerance

  @tolerance.setter
  def tolerance(self, value: float):
    """
    Setter for the 'tolerance' attribute.

    Args:
        value (float): The new tolerance level to set for text extraction.

    Raises:
        TypeError: If the provided value is not a float.
    """
    if not isinstance(value, float):
        raise TypeError("Tolerance must be a float.")
    self._tolerance = value

  def __str__(self) -> str:
    """
    Returns a string representation of the TextExtractor object.

    Returns:
        str: A string representation of the object.
    """
    return f"TextExtractor(device={self.device}, lang={self.lang}, tolerance={self.tolerance})"

  def _get_text_and_equations_with_ocr(self, equation_text_image: Image) -> str:
    """
    Extracts text and equations from a given image using Optical Character Recognition (OCR).

    Args:
        equation_text_image (Image): The cropped image containing the text and equations to be extracted.

    Returns:
        str: The extracted text and equations content.

    Raises:
        TypeError: If the type of the equation_text_image is not PIL.Image.

    """

    # Verify the input variable type
    if not isinstance(equation_text_image, Image.Image):
        raise TypeError("equation_text_image must be a PIL.Image object")

    # Get OCR results for the text image
    ocr_results = self.text_equations_ocr(equation_text_image)

    # Loop through each OCR result box to process text and equations
    for box in ocr_results:
        if box['type'] == 'text':
            # Extract and normalize coordinates from the OCR box
            x_min, y_min, x_max, y_max = self._extract_coordinates(box)

            # Crop the image based on the coordinates to get the phrase
            cropped_phrase_image = equation_text_image.crop((x_min, y_min, x_max, y_max))

            # Use OCR to extract text from the cropped phrase image
            extracted_text = self.text_ocr(cropped_phrase_image)

            # Remove newline characters from the extracted text
            extracted_text = extracted_text.replace('\n', '')

            # Update the OCR box with the extracted text
            box['text'] = extracted_text

    # Merge the extracted texts into a single string
    final_extracted_text = self._merge_line_texts(ocr_results)

    return final_extracted_text

  def _get_text_with_ocr(self, cropped_text_image: Image) -> str:
    """
    Extracts text from a given image using Optical Character Recognition (OCR).

    Args:
        cropped_text_image (Image): The cropped image containing the text to be extracted.

    Returns:
        str: The extracted text content.

    Raises:
        TypeError: If the type of the cropped_text_image is not PIL.Image.

    """

    # Verify the input variable type
    if not isinstance(cropped_text_image, Image.Image):
        raise TypeError("cropped_text_image must be a PIL.Image object")

    # Use OCR to extract text from the image
    extracted_text = self.text_ocr(cropped_text_image)

    return extracted_text

  def _get_text_without_ocr(self, text_element: TextElement, cropped_image: Image, pdf_page: Page) -> str:
    """
    Extracts text from a given area in a PDF page without using OCR.

    Args:
        text_element (TextElement): The text element containing the coordinates for text extraction.
        cropped_image (Image): The cropped image containing the text.
        pdf_page (Page): The PDF page from which the text is to be extracted.

    Returns:
        str: The extracted text content.

    Raises:
        TypeError: If the types of the arguments are not as expected.
    """

    # Verify the input variable types
    if not isinstance(text_element, TextElement):
        raise TypeError("text_element must be an instance of TextElement")
    if not isinstance(cropped_image, Image.Image):
        raise TypeError("cropped_image must be a PIL.Image object")
    if not isinstance(pdf_page, Page):
        raise TypeError("pdf_page must be an instance of pdfplumber.Page")

    # Get the dimensions of the PDF page
    pdf_width, pdf_height = pdf_page.width, pdf_page.height

    # Calculate the coordinates for text extraction based on the TextElement
    x_min_coord = int(text_element.x_min * pdf_width)
    y_min_coord = int(text_element.y_min * pdf_height)
    x_max_coord = int(text_element.x_max * pdf_width)
    y_max_coord = int(text_element.y_max * pdf_height)

    # Define the bounding box for cropping the PDF page
    bounding_box = (x_min_coord, y_min_coord, x_max_coord, y_max_coord)

    # Crop the PDF page based on the bounding box
    cropped_pdf_page = pdf_page.crop(bounding_box)

    # Extract text from the cropped PDF page
    extracted_text = cropped_pdf_page.extract_text(x_tolerance=self.tolerance)

    # Remove newline characters from the extracted text
    cleaned_text = extracted_text.replace('\n', '')

    return cleaned_text

  def _extract_coordinates(self, box: Dict):
    """
    Extract coordinates from the OCR box.

    Args:
        box (Dict): The OCR result box.

    Returns:
        Tuple[float, float, float, float]: Coordinates (x_min, y_min, x_max, y_max).
    """
    x_min = min(box['position'][:, 0])
    y_min = min(box['position'][:, 1])
    x_max = max(box['position'][:, 0])
    y_max = max(box['position'][:, 1])

    return x_min, y_min, x_max, y_max

  def _extract_and_normalize_coordinates(self, box: Dict, image_size: Tuple[int, int]) -> Tuple[float, float, float, float]:
    """
    Extract and normalize coordinates from the OCR box.

    Args:
        box (Dict): The OCR result box.
        image_size (Tuple[int, int]): The size of the image.

    Returns:
        Tuple[float, float, float, float]: Normalized coordinates (x_min, y_min, x_max, y_max).
    """
    x_min = min(box['position'][:, 0])
    y_min = min(box['position'][:, 1])
    x_max = max(box['position'][:, 0])
    y_max = max(box['position'][:, 1])

    # Normalizing Coordinates
    x_min /= image_size[0]
    y_min /= image_size[1]
    x_max /= image_size[0]
    y_max /= image_size[1]

    return x_min, y_min, x_max, y_max

  def _convert_to_cropped_page_referential(self, x_min: float, y_min: float, x_max: float, y_max: float, cropped_page: Page) -> Tuple[int, int, int, int]:
    """
    Convert normalized coordinates to cropped page's referential.

    Args:
        x_min, y_min, x_max, y_max (float): Normalized coordinates.
        cropped_page (Page): The cropped PDF page.

    Returns:
        Tuple[int, int, int, int]: Coordinates in the cropped page's referential.
    """
    x_min = int(x_min * cropped_page.width)
    y_min = int(y_min * cropped_page.height)
    x_max = int(x_max * cropped_page.width)
    y_max = int(y_max * cropped_page.height)

    x0, y0, _, _ = cropped_page.bbox

    return x_min + x0, y_min + y0, x_max + x0, y_max + y0

  def _merge_line_texts(self, ocr_results: List[Dict]) -> str:
    """
    Merges OCR results into a single string.

    This method takes a list of dictionaries containing OCR results and merges them into a single string.
    Each dictionary in the list is expected to contain text information, possibly among other details.

    Args:
        ocr_results (List[Dict]): A list of dictionaries containing OCR results.

    Returns:
        str: A single string that is the result of merging all the OCR text results.

    Note:
        This method currently uses the `pix2text.merge_line_texts` function for merging.
    """
    text = pix2text.merge_line_texts(ocr_results)
    return text
  def _get_text_and_equations_without_ocr(self, text_element: TextElement, text_image: Image, pdf_page: Page) -> str:
    """
    Extracts text and equations from a given text image without using OCR to extract text.

    Args:
        text_element (TextElement): The text element containing the coordinates for extraction.
        text_image (Image): The cropped text image.
        pdf_page (Page): The PDF page containing the text element.

    Returns:
        str: The extracted text content.

    Raises:
        TypeError: If the types of the arguments are not as expected.
    """
    # Verify the input variable types
    if not isinstance(text_element, TextElement):
        raise TypeError("text_element must be a TextElement object")
    if not isinstance(text_image, Image.Image):
        raise TypeError("text_image must be a PIL.Image object")
    if not isinstance(pdf_page, Page):
        raise TypeError("pdf_page must be a pdfplumber.Page object")

    # Get PDF and image dimensions
    pdf_width, pdf_height = pdf_page.width, pdf_page.height
    image_width, image_height = text_image.size

    # Calculate PDF coordinates based on text element's normalized coordinates
    x_min_pdf = int(text_element.x_min * pdf_width)
    y_min_pdf = int(text_element.y_min * pdf_height)
    x_max_pdf = int(text_element.x_max * pdf_width)
    y_max_pdf = int(text_element.y_max * pdf_height)

    # Define the PDF crop box
    pdf_box = (x_min_pdf, y_min_pdf, x_max_pdf, y_max_pdf)

    # Crop the PDF page based on the calculated coordinates
    cropped_page = pdf_page.crop(pdf_box)

    # Get OCR results for the text image
    ocr_results = self.text_equations_ocr(text_image)

    # Process each OCR result box
    for box in ocr_results:
        if box['type'] == 'text':
            # Extract and normalize coordinates from the OCR box
            x_min, y_min, x_max, y_max = self._extract_and_normalize_coordinates(box, text_image.size)

            # Convert normalized coordinates to cropped page's referential
            x_min, y_min, x_max, y_max = self._convert_to_cropped_page_referential(x_min, y_min, x_max, y_max, cropped_page)

            # Extract text from the cropped PDF page based on the calculated coordinates
            segmentation = cropped_page.crop((x_min, y_min, x_max, y_max))
            extracted_text = segmentation.extract_text(x_tolerance=self.tolerance)
            extracted_text = extracted_text.replace('\n', '')

            # Update the OCR box with the extracted text
            box['text'] = extracted_text

    # Merge the extracted texts into a single string
    final_text = self._merge_line_texts(ocr_results)

    return final_text


