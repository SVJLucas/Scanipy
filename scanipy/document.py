import os
import layoutparser as lp
import numpy as np
from .elements import TableElement, TextElement, ImageElement
import matplotlib.pyplot as plt
import pdf2image
import fitz
from PIL import Image

from typing import List, Iterator


class Document:
    """
    Represents a document containing various elements, such as images.

    Attributes:
        elements (list): A list of elements in the document.
    """

    def __init__(self):
        self.elements = {}
        self.images = []
        self.layouts = []
        self.table_extractor_data = []

    def to_markdown(self, output_folder, filename='output.md'):
        """
        Generate a Markdown document from the elements and save it to a file.

        :param output_folder: The folder where the Markdown file will be saved.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output = ""
        # print(self.elements)
        sorted_pages = sorted(list(self.elements.keys()))
        for page in sorted_pages:
            sorted_elements = self.get_ordered_elements(page)
            for element in sorted_elements:
                element_output = element.generate_markdown(output_folder)
                output += element_output

        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w') as f:
            f.write(output)

    def get_ordered_elements(self, page):
        return sorted(self.elements[page])

    def add_element(self, page, element):
        if self.elements.get(page) is None:
            self.elements[page] = []
        self.elements[page].append(element)

    def visualize_pipeline(self, page=0, step=0):
        if step == 0:
            return lp.draw_box(self.images[page], self.layouts[page], box_width=5, box_alpha=0.2)
        if step == 1:
            self._visualize_tables(self.table_extractor_data[page]['image'],
                                   self.table_extractor_data[page]['detected_tables'])
            return
        raise ValueError(f'step {step} not recognized')

    def visualize_block(self, page=0, block=0):
        block = self.layouts[page][block]
        segment_image = (block
                         .pad(left=5, right=15, top=5, bottom=5)
                         .crop_image(np.asarray(self.images[page])))
        return block

    def _visualize_tables(self, image, detected_tables):
        # Create a matplotlib figure and axis for visualization
        fig, ax = plt.subplots(1)
        # Display the RGB image
        ax.imshow(image)

        # Loop through each detected table to draw its bounding box
        for table in detected_tables:
            xmin, ymin, xmax, ymax = table['box'].values()

            # Create a red rectangle around the table
            rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='r', facecolor='none')

            # Add the rectangle to the plot
            ax.add_patch(rect)

            # Add label and confidence score
            label = f"{table['label']} ({table['score']:.2f})"
            plt.text(xmin, ymin, label, color='white', fontsize=12, bbox=dict(facecolor='red', alpha=0.5))

        # Hide axes and show the plot
        plt.axis('off')
        plt.show()

    def store_page(self, image, layout):
        self.layouts.append(layout)
        self.images.append(image)

    def save_tables(self, image, detected_tables):
        self.table_extractor_data.append({'image': image, 'detected_tables': detected_tables})



class PDFPage:
    def __init__(self, image: Image.Image, pdf_page: fitz.Page, page_number: int) -> None:
        self.image: Image.Image = image
        self.pdf_page: fitz.Page = pdf_page
        self.page_number: int = page_number
    
    def get_image(self) -> Image.Image:
        """Get an image of the page.

        Returns:
            PIL.Image.Image: A PIL.Image.Image object.
        """
        return self.image
    
    def get_fitz(self) -> fitz.Page:
        """Get the PyMuPDF Page object representing a page of the PDF.

        Returns:
            fitz.Page: A PyMuPDF Page object.
        """
        return self.pdf_page

class PDFDocument:
    """Represents a PDF document.

    Args:
        filepath (str): The path to the PDF file.

    Attributes:
        pdf_file (fitz.Document): A PyMuPDF Document object representing the PDF file.
        pages (List[PDFPage]): A list of PDFPage objects representing pages in the PDF.
    """
    def __init__(self, filepath: str):
        self.pdf_file: fitz.Document = fitz.open(filepath)
        self.pages: List[PDFPage] = self._initialize_pages(filepath)

    def _initialize_pages(self, filepath: str) -> List[PDFPage]:
        """Initialize and return a list of PDFPage objects for each page in the PDF.

        Returns:
            List[PDFPage]: A list of PDFPage objects.
        """
        images = pdf2image.convert_from_path(filepath)
        pages = []
        for page_number, pdf_page in enumerate(self.pdf_file):
            width = pdf_page.rect.width
            height = pdf_page.rect.height
            image = images[page_number]
            pages.append(PDFPage(image, pdf_page, page_number))
        return pages

    def __iter__(self) -> Iterator[PDFPage]:
        """Iterator method to iterate over pages in the PDF.

        Returns:
            Iterator[PDFPage]: An iterator over PDFPage objects.
        """
        self.current_page_index = 0
        return self

    def __next__(self) -> PDFPage:
        """Get the next page in the PDF.

        Returns:
            PDFPage: The next page in the PDF.
        
        Raises:
            StopIteration: If there are no more pages to iterate.
        """
        if self.current_page_index < len(self.pages):
            current_page = self.pages[self.current_page_index]
            self.current_page_index += 1
            return current_page
        else:
            raise StopIteration
