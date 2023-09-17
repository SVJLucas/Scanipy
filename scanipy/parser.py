import fitz
import logging

from .pdfhandler import PDFDocument
from .deeplearning.models import LayoutDetector, EquationFinder
from .elements import TitleElement, TextElement, TableElement, EquationElement, TitleElement, ImageElement
from .extractors import TitleExtractor, TextExtractor, TableDataExtractor, EquationExtractor, ImageExtractor
from .document import Document
from collections import defaultdict
import os


class Parser:
    """
    Parses a PDF file using PyMuPDF (fitz) and extracts its content into a Markdown file.

    Attributes:
        pdf_file (PyMuPDF.Document): The PyMuPDF Document object representing the PDF file.
    """

    def __init__(self): #TODO define device here
        """
        Initialize a new Parser instance.

        :param path: The path to the PDF file to parse.
        """
        self.layout_detector = LayoutDetector(device='cuda')
        self.table_extractor = TableDataExtractor()
        self.text_extractor = TextExtractor(use_ocr=False)
        self.title_extractor = TitleExtractor(use_ocr=False)
        self.image_extractor = ImageExtractor()
        self.equation_finder = EquationFinder(device='gpu')
        self.equation_extractor = EquationExtractor()
        # self.pipeline = [self.text_extractor, self.table_extractor, self.equation_extractor]
    
    def extract(self, path): #TODO add min and max pages
        pdfdoc = PDFDocument(path)
        elements_h = {}
        document = Document()
        image_number = 0

        for page in pdfdoc:
            elements = self.layout_detector(page.get_image())
            equations = self.equation_finder(page.get_image())

            logging.info(f'Detected {len(elements)} elements and {len(equations)} equations')

            for equation in equations:
                if equation.is_inside_text:
                    for element in elements:
                        if equation.is_in(element):
                            element.has_equation_inside = True
                            element.equation_inside = equation
                            break #TODO: what if two elements have the same equation? #BUG
            
            for element in elements:
                if isinstance(element, TextElement):
                    element = self.text_extractor.extract(page, element)
                elif isinstance(element, TableElement):
                    element = self.table_extractor.extract(page, element)
                elif isinstance(element, TitleElement):
                    element = self.title_extractor.extract(page, element)
                elif isinstance(element, ImageElement):
                    element = self.image_extractor.extract(page, element, unique_key=str(image_number))
                    image_number += 1

                document.add_element(page.page_number, element)
            for equation in equations:
                equation = self.equation_extractor.extract(page, equation)
                document.add_element(page.page_number, equation)
            elements_h[page.page_number] = [*elements,*equations]

        return document #elements_h
        
