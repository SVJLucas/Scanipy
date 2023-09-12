import fitz
from .extractors import Extractor
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
        self.extractor = Extractor()

    def extract(self, path):
        return self.extractor.extract(path)
