import fitz
from .deeplearning.models import LayoutDetector
from .elements import TextElement, TableElement, EquationElement, TitleElement, ImageElement
from .extractors import TextExtractor, TableDataExtractor, EquationExtractor, ImageExtractor
from .document import PDFDocument, Document
import os


class Parser:
    """
    Parses a PDF file using PyMuPDF (fitz) and extracts its content into a Markdown file.

    Attributes:
        pdf_file (PyMuPDF.Document): The PyMuPDF Document object representing the PDF file.
    """

    def __init__(self):
        """
        Initialize a new Parser instance.

        :param path: The path to the PDF file to parse.
        """
        self.layout_detector = LayoutDetector(device='cuda')
        self.table_extractor = TableDataExtractor()
        self.text_extractor = TextExtractor(use_ocr=False)
        self.image_extractor = ImageExtractor()
        self.equation_extractor = EquationExtractor()
        self.extractor_map = {TextElement: self.text_extractor,
                              TableElement: self.table_extractor,
                              EquationElement: self.equation_extractor,
                              TitleElement: self.text_extractor,
                              ImageElement: self.image_extractor}
        # self.pipeline = [self.text_extractor, self.table_extractor, self.equation_extractor]

    def extract(self, path):
        pdfdoc = PDFDocument(path)
        document = Document()

        for page in pdfdoc:
            elements = self.layout_detector(page.get_image())
            for element in elements:
                self.extractor_map[type(element)].extract(page.get_fitz(), page.get_image(), element)
                document.add_element(page.page_number, element)

        return document
        
