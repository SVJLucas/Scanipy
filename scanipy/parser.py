import fitz
from .extractors import Extractor
import os


class Parser:
    """
    Parses a PDF file using PyMuPDF (fitz) and extracts its content into a Markdown file.

    Attributes:
        pdf_file (PyMuPDF.Document): The PyMuPDF Document object representing the PDF file.
    """

    def __init__(self, path):
        """
        Initialize a new Parser instance.

        :param path: The path to the PDF file to parse.
        """
        self.pdf_file = fitz.open(path)
        self.path = path

    def save_markdown(self, output_folder):
        """
        Parse the PDF file, extract its content, and save it as a Markdown file.

        :param output_folder: The folder where the Markdown file will be saved.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        extractor = Extractor(self.pdf_file, self.path)
        document = extractor.extract()
        document.to_markdown(output_folder)
