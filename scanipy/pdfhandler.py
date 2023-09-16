from PIL import Image, ImageDraw
from pdfplumber.page import Page
import pdf2image
from typing import Tuple


from typing import Iterator, List


class PDFPage:
    def __init__(self, image: Image.Image, pdf_page: Page, page_number: int) -> None:
        self.image: Image.Image = image
        self.pdf_page: Page = pdf_page
        self.page_number: int = page_number

    def get_image(self) -> Image.Image:
        """Get an image of the page.

        Returns:
            PIL.Image.Image: A PIL.Image.Image object.
        """
        return self.image

    def get_fitz(self) -> Page:
        """Get the PyMuPDF Page object representing a page of the PDF.

        Returns:
            fitz.Page: A PyMuPDF Page object.
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
        xmin, ymin, xmax, ymax = coordinates  # Unpack the coordinates tuple

        # Get the dimensions (width and height) of the image
        img_width, img_height = self.image.size

        # Scale the coordinates to match the image size
        x1 = xmin * img_width
        y1 = ymin * img_height
        x2 = xmax * img_width
        y2 = ymax * img_height

        # Create a copy of the page image to avoid modifying the original
        modified_image = self.image.copy()

        # Create a drawing context on the copy of the image
        draw = ImageDraw.Draw(modified_image)

        # Draw the rectangle on the copy of the image
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

        # Display or save the modified image as needed
        # You can add code here to display or save the image if necessary

        return modified_image

class PDFDocument:
    """Represents a PDF document.

    Args:
        filepath (str): The path to the PDF file.

    Attributes:
        pdf_file (fitz.Document): A PyMuPDF Document object representing the PDF file.
        pages (List[PDFPage]): A list of PDFPage objects representing pages in the PDF.
    """
    def __init__(self, filepath: str):
        self.pdf_file: fitz.Document = fitz.open(filepath)
        self.pages: List[PDFPage] = self._initialize_pages(filepath)

    def _initialize_pages(self, filepath: str) -> List[PDFPage]:
        """Initialize and return a list of PDFPage objects for each page in the PDF.

        Returns:
            List[PDFPage]: A list of PDFPage objects.
        """
        images = pdf2image.convert_from_path(filepath)
        pages = []
        for page_number, pdf_page in enumerate(self.pdf_file):
            width = pdf_page.rect.width
            height = pdf_page.rect.height
            image = images[page_number]
            pages.append(PDFPage(image, pdf_page, page_number))
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