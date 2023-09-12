from .document import Document
from .imageextractor import ImageExtractor
from .tabledataextractor import TableDataExtractor
from .text import TextExtractor

class Extractor:
    """
    Extracts content from a PDF file and creates a Document object.

    Attributes:
        pdf_file (str): The path to the PDF file to extract content from.
        image_extractor (ImageExtractor): An instance of ImageExtractor to extract images.
    """

    def __init__(self, pdf_file, filepath):
        """
        Initialize a new Extractor instance.

        :param pdf_file: The path to the PDF file to extract content from.
        """
        self.pdf_file = pdf_file
        self.image_extractor = ImageExtractor(pdf_file)
        self.table_extractor = TableDataExtractor()
        self.text_extractor = TextExtractor(filepath)

    def extract(self):
        """
        Extract content from the PDF file, including images, and create a Document object.

        :return: A Document object containing extracted content.
        """
        document = Document()
        # self.image_extractor.get_images(document)
        self.text_extractor.extract(document)
        # for page_index, page in enumerate(self.pdf_file):
        #     print(self.table_extractor.tables_from_page(page))
        return document
