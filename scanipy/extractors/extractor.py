from scanipy.document import Document
from .tabledataextractor import TableDataExtractor
from .text import TextExtractor

class Extractor:
    """
    Extracts content from a PDF file and creates a Document object.

    Attributes:
        pdf_file (str): The path to the PDF file to extract content from.
        image_extractor (ImageExtractor): An instance of ImageExtractor to extract images.
    """

    def __init__(self):
        """
        Initialize a new Extractor instance.
        """
        self.table_extractor = TableDataExtractor()
        self.text_extractor = TextExtractor()

    def extract(self, filepath):
        """
        Extract content from the PDF file, including images, and create a Document object.

        :param pdf_file: The path to the PDF file to extract content from.
        :return: A Document object containing extracted content.
        """
        document = Document()
        self.text_extractor.extract(filepath, document)
        # for page_index, page in enumerate(self.pdf_file):
        #     print(self.table_extractor.tables_from_page(page))
        return document
