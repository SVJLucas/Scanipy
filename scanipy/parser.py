import fitz
from .extractors import TextExtractor, TableDataExtractor
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
        self.text_extractor = TextExtractor()
        self.pipeline = [self.text_extractor, self.table_extractor]

    def extract(self, path):
        document = Document()
        for step in self.pipeline:
            step.extract(path, document)
        return document
