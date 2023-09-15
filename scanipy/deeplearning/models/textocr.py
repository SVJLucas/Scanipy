import fitz
from PIL import Image

# PIL.Image.LINEAR = PIL.Image.BILINEAR
# DPI = 200
# IMAGE_TO_FITZ_CONSTANT = 72 / DPI

class TextOCR:

    def __init__(self, lang='en', use_ocr=False):
        self.use_ocr = use_ocr

    def __call__(self, page, image, dimensions, image_to_fitz_constant):
        if self.use_ocr:
            pass #TODO
        else:
            return self.extract_text_from_pdf(page, dimensions, image_to_fitz_constant)
        
    def extract_text_from_pdf(self, page, dimensions, image_to_fitz_constant):
        dimensions = [d*image_to_fitz_constant for d in dimensions]
        crop_rect = fitz.Rect(*dimensions)

        text = page.get_text("text", clip=crop_rect).strip().replace('\n', ' ')
        return text
    
    def print_text_block(self, page, rect):
        """Draw a rectangle on a PyMuPDF Page object.

        Args:
            pdf_page (fitz.Page): A PyMuPDF Page object.
            x1 (float): The x-coordinate of the first point.
            y1 (float): The y-coordinate of the first point.
            x2 (float): The x-coordinate of the second point.
            y2 (float): The y-coordinate of the second point.
        """

        # Create a red outline for the rectangle
        page.draw_rect(rect, color=(1, 0, 0), width=2)

        pixmap = page.get_pixmap()
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        img.show()
        input()