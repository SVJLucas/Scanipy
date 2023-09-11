from .document import Document
from .imageextractor import ImageExtractor


class Extractor:
    """
    Extracts content from a PDF file and creates a Document object.

    Attributes:
        pdf_file (str): The path to the PDF file to extract content from.
        image_extractor (ImageExtractor): An instance of ImageExtractor to extract images.
    """

    def __init__(self, pdf_file):
        """
        Initialize a new Extractor instance.

        :param pdf_file: The path to the PDF file to extract content from.
        """
        self.pdf_file = pdf_file
        self.image_extractor = ImageExtractor(pdf_file)

    def extract(self):
        """
        Extract content from the PDF file, including images, and create a Document object.

        :return: A Document object containing extracted content.
        """
        document = Document()
        self.image_extractor.get_images(document)
        return document
