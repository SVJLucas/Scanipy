from typing import Union
from PIL import Image
from scanipy.deeplearning.models import TableStructureAnalyzer
from scanipy.elements import TableElement
from .extractor import Extractor

from math import ceil, floor
import numpy as np
import pandas as pd
import cv2
import pytesseract

# Define the TableDataExtractor class
class TableDataExtractor(Extractor):
    """
    Represents an table extractor for extracting tables from a document.

    Attributes:
        latex_ocr (str): Deep Learning Model to extract tables from images.
    """

    def __init__(self, table_expansion_margin=10, threshold_percentage=0.10):
        """
        Initialize an TableDataExtractor object.
        """
        # Initialize the model for identifying table structures
        self.model = TableStructureAnalyzer()

        # Expand the bounding box slightly for better cropping
        self._table_expansion_margin = table_expansion_margin

        # Use a percentage (e.g., 10%) of the average height as the threshold for a new row
        self._threshold_percentage = threshold_percentage
        self.test = []

    def _get_cell_coordinates(self, page_image, table_element):
        """
        Obtains the coordinates of cells based on the analyzed table structure.

        Args:
            analyzed_structure (List[Dict]): Analyzed table structure.

        Returns:
            List[Dict]: List of cell coordinates.
        """
        # Convert PIL image to OpenCV format
        image_cv = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

        # Get image dimensions
        img_height, img_width = image_cv.shape[:2]

        # Expand the bounding box slightly for better cropping
        xmin, ymin = max(0, table_element.x_min - self._table_expansion_margin), max(0, table_element.y_min - self._table_expansion_margin)
        xmax, ymax = min(img_width, table_element.x_max + self._table_expansion_margin), min(img_height, table_element.y_max + self._table_expansion_margin)

        # Crop the image based on the coordinates
        table_image = page_image.crop((xmin, ymin, xmax, ymax))

        # Extract the structure from the cropped table image
        table_structure = self.model(table_image)
        
        # For some reason, this improves the cell boxes #FIXME
        for box in table_structure:
            box['box']['ymax'] =  box['box']['ymax'] + 5

        # Extract row and column bounding boxes from the table structure
        rows = [box['box'] for box in table_structure if box['label'] == 'table row']
        columns = [box['box'] for box in table_structure if box['label'] == 'table column']


        # Initialize a list to store cell positions
        cells = []

        # Loop through each row and column to find overlapping regions as cells
        #TODO: adapt for different table layouts
        for row in rows:
            for column in columns:
                cell_xmin = max(row['xmin'], column['xmin'])
                cell_ymin = max(row['ymin'], column['ymin'])
                cell_xmax = min(row['xmax'], column['xmax'])
                cell_ymax = min(row['ymax'], column['ymax'])

                # Add the cell only if it has a non-zero area
                if cell_xmin < cell_xmax and cell_ymin < cell_ymax:
                    cells.append({
                        'xmin': xmin + cell_xmin,
                        'ymin': ymin + cell_ymin,
                        'xmax': xmin + cell_xmax,
                        'ymax': ymin + cell_ymax
                    })
        # print(cells)
        return cells
    
    def _get_dataframe(self, rows, page_image):
        # Initialize an empty DataFrame
        df = pd.DataFrame()

        # Populate the DataFrame
        for row_idx, row_boxes in enumerate(rows):
            row_data = []
            for col_idx, box in enumerate(row_boxes):
                image_cv = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
                text = self.get_text_from_image(image_cv, box)
                row_data.append(text)

            # If it's the first row, set the DataFrame columns
            if row_idx == 0:
                df = pd.DataFrame(columns=row_data)
            else:
                df.loc[row_idx - 1] = row_data
        
        return df
    
    def _pad_image_with_white(self, image_cv, pad):

        # Get the dimensions of the original image
        height, width, _ = image_cv.shape

        # Calculate the dimensions of the new padded image
        padded_height = height + pad + pad
        padded_width = width + pad + pad

        # Create white image
        padded_image = np.ones((padded_height, padded_width, 3), dtype=np.uint8) * 255

        # Paste the original image onto the canvas with padding
        padded_image[pad:pad + height, pad:pad + width] = image_cv

        return padded_image
    
    def _remove_table_lines(self, image_cv):
        # Convert to grayscale
        image_cv_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

        # Use Hough Line Transform to detect lines
        edges = cv2.bitwise_not(image_cv_gray).astype('uint8')
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)

        # Draw the detected lines on a copy of the original image
        cleaned_image = image_cv.copy()
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(cleaned_image, (x1, y1), (x2, y2), (255, 255, 255), 6)

        return cleaned_image


    def _separate_rows(self, cell_coordinates):
        # Sort boxes by ymin to separate rows
        cell_coordinates = sorted(cell_coordinates, key=lambda x: x['ymin'])

        # Calculate the average height of all boxes
        avg_height = np.mean([box['ymax'] - box['ymin'] for box in cell_coordinates])

        # Use a percentage (e.g., 10%) of the average height as the threshold for a new row
        threshold = self._threshold_percentage * avg_height

        # Identify unique rows by their y-coordinates
        rows = []
        last_ymin = None
        for box in cell_coordinates:
            ymin = box['ymin']
            if last_ymin is None or abs(ymin - last_ymin) > threshold:  # Adjust the threshold as needed
                rows.append([])
            rows[-1].append(box)
            last_ymin = ymin

        # Sort each row by xmin to arrange columns
        for row in rows:
            row.sort(key=lambda x: x['xmin'])

        return rows

    def get_text_from_image(self, image_cv, box):
        xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']

        # Extract each cell image
        # cell_image = image_cv[ymin:ymax, xmin:xmax]
        cell_image = image_cv[floor(ymin):ceil(ymax), floor(xmin):ceil(xmax)]

        text = ''
        for pad in [3,8,13,20]: # don't ask me why, but some numbers can only be read with a SPECIFIC padding #FIXME #despair
            # Pad image with white to improve OCR
            cell_image_padded = self._pad_image_with_white(cell_image, pad)
            
            # Clean the table lines to improve OCR performance
            cell_image_padded = self._remove_table_lines(cell_image_padded)

            # Convert to PIL Image
            cell_image_padded_pil = Image.fromarray(cv2.cvtColor(cell_image_padded, cv2.COLOR_BGR2RGB))

            # Perform OCR to get text
            text = pytesseract.image_to_string(cell_image_padded_pil).strip().replace('\n', '')

            if text != '':
                break

        return text

    def extract(self, page_image: Image, table_element: TableElement) -> TableElement:
        """
        Extracts an table from a given page image based on the coordinates in the table element.

        Args:
            page_image (PIL.Image): The page image from which to extract the table.
            table_element (TableElement): The table element containing the coordinates for extraction.

        Returns:
            TableElement: The updated table element with the extracted LaTeX content.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not isinstance(page_image, Image.Image):
            raise TypeError("page_image must be a PIL.Image object")
        if not isinstance(table_element, TableElement):
            raise TypeError("table_element must be an TableElement object") #TODO

        # Gather the individual cells from the table
        cell_coordinates = self._get_cell_coordinates(page_image, table_element)

        rows = self._separate_rows(cell_coordinates)

        dataframe = self._get_dataframe(rows, page_image)

        # Update the table element with the extracted LaTeX content
        table_element._table_data = dataframe

        return table_element

    def __str__(self) -> str:
        """
        Returns a string representation of the TableDataExtractor object.

        Returns:
            str: A string representation of the object.
        """
        return f"TableDataExtractor(latex_ocr={self.latex_ocr})"
