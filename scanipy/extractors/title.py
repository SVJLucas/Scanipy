import torch
import pix2text
from PIL import Image
from pdfplumber.page import Page
from .extractor import Extractor
from scanipy.pdfhandler import PDFPage
from scanipy.elements import TitleElement 
from scanipy.deeplearning import TextOCR
from typing import Union, Tuple, List, Dict


# Define the TitleExtractor class
class TitleExtractor(Extractor):
    """
    Represents a title extractor for extracting title from a document.
    """

    def __init__(self, use_ocr: bool, lang: str = 'en', tolerance: float = 1.5):
      """
      Initialize a TitleExtractor object.

      Args:
          use_ocr (bool): Whether to use OCR for title extraction or not.
          lang (str): The language of the title. Defaults to english.
          tolerance (float): The tolerance level for title extraction. Default is 1.5.

      Raises:
          TypeError: If the types of the arguments are not as expected.
      """

      # Verify the input variable types
      if not isinstance(use_ocr, bool):
          raise TypeError("use_ocr must be a boolean")

      # Initialize OCR settings and OCR model
      self.use_ocr = use_ocr

      # Check if CUDA is available and set the device accordingly
      self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

      # Initialize OCR model for title and equations
      self.title_equations_ocr = pix2text.Pix2Text(device=self.device)

      # Set the language for OCR
      self.lang = lang

      # Initialize the TextOCR object
      self.title_ocr = TextOCR(self.lang, self.device)

      # Set the tolerance level for title extraction
      self.tolerance = tolerance

    def _process_title_image(self, title_element: TitleElement, title_image: Image, pdf_page: Page) -> str:
      """
      Process the title image based on OCR settings and equation presence.

      Args:
          title_element (TitleElement): The title element containing the coordinates for extraction.
          title_image (Image): The cropped title image.
          pdf_page (Page): The PDF page containing the title element.

      Returns:
          str: The extracted title content.
      """
      # Use OCR or not based on the use_ocr flag and whether the title element contains equations
      if self.use_ocr:
          if title_element.has_equation_inside:
              return self._get_title_and_equations_with_ocr(title_image)
          else:
              return self._get_title_with_ocr(title_image)
      else:
          if title_element.has_equation_inside:
              return self._get_title_and_equations_without_ocr(title_element, title_image, pdf_page)
          else:
              return self._get_title_without_ocr(title_element, title_image, pdf_page)

    def extract(self, page: PDFPage, page_image: Image, title_element: TitleElement) -> TitleElement:
        """
        Extracts title from a given page image based on the coordinates in the title element.

        Args:
            pdf_page (Page): The PDF page from which to extract the title.
            page_image (Image): The page image from which to extract the title.
            title_element (TitleElement): The title element containing the coordinates for extraction.

        Returns:
            TitleElement: The updated title element with the extracted title content.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Separate PIL and pdfplumber elements from the 
        pdf_page = page.get_pdf()
        page_image = page.get_image()

        # Verify the input variable types
        if not isinstance(page_image, Image.Image):
            raise TypeError("page_image must be a PIL.Image object")
        if not isinstance(title_element, TitleElement):
            raise TypeError("title_element must be a TitleElement object")

        # Extract the coordinates from the title element
        left = title_element.x_min * page_image.width
        upper = title_element.y_min * page_image.height
        right = title_element.x_max * page_image.width
        lower = title_element.y_max * page_image.height

        # Crop the image based on the coordinates
        title_image = page_image.crop((left, upper, right, lower))

        # Process the cropped title image and extract the title content
        title_content = self._process_title_image(title_element, title_image, pdf_page)

        # Update the title element with the extracted title content
        title_element.title_content = title_content

        return title_element

    def __str__(self) -> str:
        """
        Returns a string representation of the TitleExtractor object.

        Returns:
            str: A string representation of the object.
        """
        return f"TitleExtractor(use_ocr={self.use_ocr}, device={self.device}, lang={self.lang}, tolerance={self.tolerance}, title_ocr={self.title_ocr})"

    @property
    def tolerance(self) -> float:
        """
        Getter for the 'tolerance' attribute.

        Returns:
            float: The current tolerance level for title extraction.
        """
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value: float):
        """
        Setter for the 'tolerance' attribute.

        Args:
            value (float): The new tolerance level to set for title extraction.

        Raises:
            TypeError: If the provided value is not a float.
        """
        if not isinstance(value, float):
            raise TypeError("Tolerance must be a float.")
        self._tolerance = value

    def _get_title_and_equations_with_ocr(self, equation_title_image: Image) -> str:
        """
        Extracts title and equations from a given image using Optical Character Recognition (OCR).

        Args:
            equation_title_image (Image): The cropped image containing the title and equations to be extracted.

        Returns:
            str: The extracted title and equations content.

        Raises:
            TypeError: If the type of the equation_title_image is not PIL.Image.

        """

        # Verify the input variable type
        if not isinstance(equation_title_image, Image.Image):
            raise TypeError("equation_title_image must be a PIL.Image object")

        # Get OCR results for the title image
        ocr_results = self.title_equations_ocr(equation_title_image)

        # Loop through each OCR result box to process title and equations
        for box in ocr_results:
            if box['type'] == 'text':
                # Extract and normalize coordinates from the OCR box
                x_min, y_min, x_max, y_max = self._extract_coordinates(box)

                # Crop the image based on the coordinates to get the phrase
                cropped_phrase_image = equation_title_image.crop((x_min, y_min, x_max, y_max))

                # Use OCR to extract title from the cropped phrase image
                extracted_title = self.title_ocr(cropped_phrase_image)

                # Remove newline characters from the extracted title
                extracted_title = extracted_title.replace('\n', '')

                # Update the OCR box with the extracted title
                box['text'] = extracted_title

        # Merge the extracted titles into a single string
        final_extracted_title = self._merge_line_titles(ocr_results)

        return final_extracted_title

    def _get_title_with_ocr(self, cropped_title_image: Image) -> str:
        """
        Extracts title from a given image using Optical Character Recognition (OCR).

        Args:
            cropped_title_image (Image): The cropped image containing the title to be extracted.

        Returns:
            str: The extracted title content.

        Raises:
            TypeError: If the type of the cropped_title_image is not PIL.Image.

        """

        # Verify the input variable type
        if not isinstance(cropped_title_image, Image.Image):
            raise TypeError("cropped_title_image must be a PIL.Image object")

        # Use OCR to extract title from the image
        extracted_title = self.title_ocr(cropped_title_image)

        return extracted_title

    def _get_title_without_ocr(self, title_element: TitleElement, cropped_image: Image, pdf_page: Page) -> str:
        """
        Extracts title from a given area in a PDF page without using OCR.

        Args:
            title_element (TitleElement): The title element containing the coordinates for title extraction.
            cropped_image (Image): The cropped image containing the title.
            pdf_page (Page): The PDF page from which the title is to be extracted.

        Returns:
            str: The extracted title content.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """

        # Verify the input variable types
        if not isinstance(title_element, TitleElement):
            raise TypeError("title_element must be an instance of TitleElement")
        if not isinstance(cropped_image, Image.Image):
            raise TypeError("cropped_image must be a PIL.Image object")
        if not isinstance(pdf_page, Page):
            raise TypeError("pdf_page must be an instance of pdfplumber.Page")

        # Get the dimensions of the PDF page
        pdf_width, pdf_height = pdf_page.width, pdf_page.height

        # Calculate the coordinates for title extraction based on the TitleElement
        x_min_coord = int(title_element.x_min * pdf_width)
        y_min_coord = int(title_element.y_min * pdf_height)
        x_max_coord = int(title_element.x_max * pdf_width)
        y_max_coord = int(title_element.y_max * pdf_height)

        # Define the bounding box for cropping the PDF page
        bounding_box = (x_min_coord, y_min_coord, x_max_coord, y_max_coord)

        # Crop the PDF page based on the bounding box
        cropped_pdf_page = pdf_page.crop(bounding_box)

        # Extract title from the cropped PDF page
        extracted_title = cropped_pdf_page.extract_text(x_tolerance=self.tolerance)

        # Remove newline characters from the extracted title
        cleaned_title = extracted_title.replace('\n', '')

        return cleaned_title

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

    def _merge_line_titles(self, ocr_results: List[Dict]) -> str:
        """
        Merges OCR results into a single string.

        This method takes a list of dictionaries containing OCR results and merges them into a single string.
        Each dictionary in the list is expected to contain title information, possibly among other details.

        Args:
            ocr_results (List[Dict]): A list of dictionaries containing OCR results.

        Returns:
            str: A single string that is the result of merging all the OCR title results.

        Note:
            This method currently uses the `pix2text.merge_line_texts` function for merging.
        """
        text = pix2text.merge_line_texts(ocr_results)
        return text

    def _get_title_and_equations_without_ocr(self, title_element: TitleElement, title_image: Image, pdf_page: Page) -> str:
        """
        Extracts title and equations from a given title image without using OCR to extract title.

        Args:
            title_element (TitleElement): The title element containing the coordinates for extraction.
            title_image (Image): The cropped title image.
            pdf_page (Page): The PDF page containing the title element.

        Returns:
            str: The extracted title content.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not isinstance(title_element, TitleElement):
            raise TypeError("title_element must be a TitleElement object")
        if not isinstance(title_image, Image.Image):
            raise TypeError("title_image must be a PIL.Image object")
        if not isinstance(pdf_page, Page):
            raise TypeError("pdf_page must be a pdfplumber.Page object")

        # Get PDF and image dimensions
        pdf_width, pdf_height = pdf_page.width, pdf_page.height
        image_width, image_height = title_image.size

        # Calculate PDF coordinates based on title element's normalized coordinates
        x_min_pdf = int(title_element.x_min * pdf_width)
        y_min_pdf = int(title_element.y_min * pdf_height)
        x_max_pdf = int(title_element.x_max * pdf_width)
        y_max_pdf = int(title_element.y_max * pdf_height)

        # Define the PDF crop box
        pdf_box = (x_min_pdf, y_min_pdf, x_max_pdf, y_max_pdf)

        # Crop the PDF page based on the calculated coordinates
        cropped_page = pdf_page.crop(pdf_box)

        # Get OCR results for the title image
        ocr_results = self.title_equations_ocr(title_image)

        # Process each OCR result box
        for box in ocr_results:
            if box['type'] == 'text':
                # Extract and normalize coordinates from the OCR box
                x_min, y_min, x_max, y_max = self._extract_and_normalize_coordinates(box, title_image.size)

                # Convert normalized coordinates to cropped page's referential
                x_min, y_min, x_max, y_max = self._convert_to_cropped_page_referential(x_min, y_min, x_max, y_max, cropped_page)

                # Extract title from the cropped PDF page based on the calculated coordinates
                segmentation = cropped_page.crop((x_min, y_min, x_max, y_max))
                extracted_title = segmentation.extract_text(x_tolerance=self.tolerance)
                extracted_title = extracted_title.replace('\n', '')

                # Update the OCR box with the extracted title
                box['text'] = extracted_title

        # Merge the extracted titles into a single string
        final_title = self._merge_line_titles(ocr_results)

        return final_title

