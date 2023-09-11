from PIL import Image
import io

class ImageExtractor:
    """
    Extract images from a PDF file using PyMuPDF and add them to a Document object.

    Attributes:
        pdf_file (PyMuPDF.PDF): The PyMuPDF PDF object representing the PDF file.
    """

    def __init__(self, pdf_file):
        """
        Initialize a new ImageExtractor instance.

        :param pdf_file: The PyMuPDF PDF object representing the PDF file.
        """
        self.pdf_file = pdf_file

    def get_images(self, document):
        """
        Extract images from each page of the PDF and add them to the Document object.

        :param document: The Document object to which the extracted images will be added.
        """
        for page_index, page in enumerate(self.pdf_file):
            image_list = page.get_images()
            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = self.pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                # Load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                document.add_image(image, image_ext)