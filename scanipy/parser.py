import fitz
from .extractors import TextExtractor, TableDataExtractor, EquationExtractor
from .document import Document
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
        self.table_extractor = TableDataExtractor()
        self.text_extractor = TextExtractor(use_cuda=True)
        self.equation_extractor = EquationExtractor()
        self.pipeline = [self.text_extractor, self.table_extractor, self.equation_extractor]

    def extract(self, path):
        document = Document()
        for step, extractor in enumerate(self.pipeline):
            extractor.extract(path, document, pipeline_step=step)
        return document
