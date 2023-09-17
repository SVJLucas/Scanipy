from PIL import Image, ImageDraw
import pdfplumber
import pdfplumber.page
from typing import Tuple, Iterator, List

def draw_rectangle(image: Image.Image, coordinates: Tuple[float, float, float, float]) -> Image.Image:
    """
    Draw a rectangle on the page image and return the modified image.

    Args:
        image (PIL.Image.Image): The image on which to draw the rectangle.
        coordinates (Tuple[float, float, float, float]): A tuple containing the coordinates
            (xmin, ymin, xmax, ymax) of the rectangle, where each coordinate is in the range [0, 1].

    Returns:
        PIL.Image.Image: A modified PIL.Image.Image object with the rectangle drawn.
    """
    xmin, ymin, xmax, ymax = coordinates  # Unpack the coordinates tuple

    # Get the dimensions (width and height) of the image
    img_width, img_height = image.size

    # Scale the coordinates to match the image size
    if 0 <= xmin <= 1:
        xmin = xmin * img_width
        ymin = ymin * img_height
        xmax = xmax * img_width
        ymax = ymax * img_height

    # Create a copy of the image to avoid modifying the original
    modified_image = image.copy()

    # Create a drawing context on the copy of the image
    draw = ImageDraw.Draw(modified_image)

    # Draw the rectangle on the copy of the image
    draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=2)

    # Display or save the modified image as needed
    # You can add code here to display or save the image if necessary

    return modified_image

class PDFPage:
    def __init__(self, image: Image.Image, pdf_page: pdfplumber.page.Page, page_number: int) -> None:
        self.image: Image.Image = image
        self.pdf_page: pdfplumber.page.Page = pdf_page
        self.page_number: int = page_number

    def get_image(self) -> Image.Image:
        """Get an image of the page.

        Returns:
            PIL.Image.Image: A PIL.Image.Image object.
        """
        return self.image

    def get_pdf(self) -> pdfplumber.page.Page:
        """Get the pdfplumber Page object representing a page of the PDF.

        Returns:
            pdfplumber.page.Page: A pdfplumber Page object.
        """
        return self.pdf_page
    
    def draw_rectangle(self, coordinates: Tuple[float, float, float, float]) -> Image.Image:
        """
        Draw a rectangle on the page image and return the modified image.

        Args:
            coordinates (Tuple[float, float, float, float]): A tuple containing the coordinates
                (xmin, ymin, xmax, ymax) of the rectangle, where each coordinate is in the range [0, 1].

        Returns:
            PIL.Image.Image: A modified PIL.Image.Image object with the rectangle drawn.
        """
        modified_image = draw_rectangle(self.image, coordinates)
        return modified_image


class PDFDocument:
    """Represents a PDF document.

    Args:
        filepath (str): The path to the PDF file.

    Attributes:
        pdf_file (pdfplumber.pdf.PDF): A pdfplumber PDF object representing the PDF file.
        pages (List[PDFPage]): A list of PDFPage objects representing pages in the PDF.
    """
    def __init__(self, filepath: str):
        self.pdf_file = pdfplumber.open(filepath)
        self.pages = self._initialize_pages()

    def _initialize_pages(self) -> List[PDFPage]:
        """Initialize and return a list of PDFPage objects for each page in the PDF.

        Returns:
            List[PDFPage]: A list of PDFPage objects.
        """
        pages = []
        for page_number, pdf_page in enumerate(self.pdf_file.pages):
            image = pdf_page.to_image(resolution=200).original.copy()
            pages.append(PDFPage(image, pdf_page, page_number + 1))
        return pages

    def __iter__(self) -> Iterator[PDFPage]:
        """Iterator method to iterate over pages in the PDF.

        Returns:
            Iterator[PDFPage]: An iterator over PDFPage objects.
        """
        self.current_page_index = 0
        return self

    def __next__(self) -> PDFPage:
        """Get the next page in the PDF.

        Returns:
            PDFPage: The next page in the PDF.

        Raises:
            StopIteration: If there are no more pages to iterate.
        """
        if self.current_page_index < len(self.pages):
            current_page = self.pages[self.current_page_index]
            self.current_page_index += 1
            return current_page
        else:
            raise StopIteration