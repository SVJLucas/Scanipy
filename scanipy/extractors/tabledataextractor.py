import cv2
import numpy as np
import pandas as pd
from PIL import Image
from typing import List, Dict
import matplotlib.pyplot as plt


from deeplearning import TableStructureAnalyzer, TableFinder


class TableDataExtractor:
    """
    A class to manage the extraction of tables from images.

    Attributes:
        _table_finder (callable): Model for identifying tables in images.
        _structure_analyzer (callable): Model for table structure analysis.
        _confidence_threshold (float): Confidence score threshold for filtering detected tables.
    """

    def __init__(self, confidence_threshold=0.990, expansion_margin=10, threshold_percentage=0.10):
        """
        Initializes TableDataExtractor with structure and detection models and a confidence threshold.

        Args:
            confidence_threshold (float, optional): Confidence score threshold for table detection. Defaults to 0.990.
        """
        # Initialize table detection and structure analysis models
        self._table_finder = TableFinder()
        self._structure_analyzer = TableStructureAnalyzer()

        # Set the confidence threshold for table detection
        self._confidence_threshold = confidence_threshold

        # Expand the bounding box slightly for better cropping
        self._expansion_margin = expansion_margin
        # Use a percentage (e.g., 10%) of the average height as the threshold for a new row
        self._threshold_percentage = threshold_percentage

    def _detect_tables(self, image):
        """
        Detect tables in a given image and filter them based on the confidence score.

        Args:
            image (PIL.Image): The input image in which to detect tables.

        Returns:
            List[Dict]: Detected tables along with bounding boxes, filtered by confidence score.
        """
        # Detect tables in the image using the table finder model
        detected_tables = self._table_finder(image)

        # Filter tables based on the confidence score threshold
        filtered_tables = [table for table in detected_tables if table['score'] >= self._confidence_threshold]

        return filtered_tables

    def visualize_tables(self, image):
        """
        Display the image with bounding boxes around detected tables.

        Args:
            image (PIL.Image): The input image in which tables were detected.
        """

        # Get the bounding boxes of detected tables
        detected_tables = self._detect_tables(image)

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

    def _extract_table_regions(self, image, detected_tables):
        """
        Crop and extract table regions from the image.

        Args:
            image (PIL.Image): The input PIL image.
            detected_tables (List[Dict]): The bounding boxes around the detected tables.

        Returns:
            List[Dict]:

                Dict keys:
                    'table':cropped table regions as PIL images.
                    'xmin':
                    'ymin':
                    'xmax':
                    'ymax'
        """
        # Convert PIL image to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Get image dimensions
        img_height, img_width = image_cv.shape[:2]

        # Initialize a list to store cropped table images
        cropped_tables = []

        # Loop through each detected table's bounding box to crop it from the original image
        for box in detected_tables:
            xmin, ymin, xmax, ymax = box['box'].values()

            # Expand the bounding box slightly for better cropping
            xmin, ymin = max(0, xmin - self._expansion_margin), max(0, ymin - self._expansion_margin)
            xmax, ymax = min(img_width, xmax + self._expansion_margin), min(img_height, ymax + self._expansion_margin)

            # Crop the table from the original image
            table_region = image_cv[ymin:ymax, xmin:xmax]

            # Convert the cropped table back to a PIL Image
            table_pil = Image.fromarray(cv2.cvtColor(table_region, cv2.COLOR_BGR2RGB))

            # Append the cropped table and its position to the list
            cropped_tables.append({'table': table_pil,
                                   'xmin': xmin,
                                   'ymin': ymin,
                                   'xmax': xmax,
                                   'ymax': ymax})

        return cropped_tables

    def _analyze_structure(self, table):
        """
        Analyzes the structure of a table in the image.

        Args:
            table (PIL.Image): The (cropped) table image.

        Returns:
            table_structure (List[Dict]): List of rows and columns with their bounding boxes.
        """
        # Run structure recognition on the table image
        plt.imshow(table)
        plt.show()
        print(len(self._detect_tables(table)))
        analyzed_structure = self._structure_analyzer(table)
        return analyzed_structure

    def _get_cell_coordinates(self, analyzed_structure, xmin=0, ymin=0):
        """
        Obtains the coordinates of cells based on the analyzed table structure.

        Args:
            analyzed_structure (List[Dict]): Analyzed table structure.

        Returns:
            List[Dict]: List of cell coordinates.
        """
        # Extract row and column bounding boxes from the table structure
        rows = [box['box'] for box in analyzed_structure if box['label'] == 'table row']
        columns = [box['box'] for box in analyzed_structure if box['label'] == 'table column']

        # Initialize a list to store cell positions
        cells = []

        # Loop through each row and column to find overlapping regions as cells
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
        print(cells)
        return cells

    def _extract_cell_coordinates_from_image(self, input_image):

        """
        Extracts the coordinates of cells from tables present in the image.

        Args:
            input_image: The image from which to extract table cell coordinates.

        Returns:
            List[List[Dict]]: A nested list of dictionaries, each containing the coordinates of cells for each detected table.

        Example:
            >>> extractor = TableDataExtractor()
            >>> extractor.extract_cell_coordinates_from_image(image)
            [
                [{'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}, ...],
                ...
            ]
        """

        # Initialize a list to hold cell coordinates for each table
        all_tables_cell_coordinates = []

        # Detect tables present in the image
        detected_tables = self._detect_tables(input_image)

        # Crop the regions of the image that contain tables
        cropped_table_images = self._extract_table_regions(input_image, detected_tables)

        # Loop through each cropped table image
        for single_table_crop_dict in cropped_table_images:
            single_table_crop = single_table_crop_dict['table']
            xmin = single_table_crop_dict['xmin']
            ymin = single_table_crop_dict['xmin']

            # Analyze the structure of the cropped table to identify rows and columns
            table_structure_analysis = self._analyze_structure(single_table_crop)

            # Get the cell coordinates based on the analyzed table structure
            cell_coordinates = self._get_cell_coordinates(table_structure_analysis, xmin, ymin)

            # Append the cell coordinates of this table to the master list
            all_tables_cell_coordinates.append(cell_coordinates)

        # Return the master list of all cell coordinates from all tables
        return all_tables_cell_coordinates

    def get_text_from_page(self, page, box, image_cv):
        xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']
        if image_cv is not None:
            # Extract each cell image
            cell_image = image_cv[ymin:ymax, xmin:xmax]

            # Convert to PIL Image
            cell_image_pil = Image.fromarray(cv2.cvtColor(cell_image, cv2.COLOR_BGR2RGB))

            # Perform OCR to get text
            text = pytesseract.image_to_string(cell_image_pil).strip()

        else:
            # Define the rectangle for cropping (x0, y0, x1, y1)
            crop_rect = fitz.Rect(xmin, ymin, xmax, ymax)

            # Extract text from the cropped area
            text = page.get_text("text", clip=crop_rect)

        return text

    def tables_from_page(self, page, is_image=False):
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        all_tables_cell_coordinates = self._extract_cell_coordinates_from_image(image)

        dataframes = []

        for boxes in all_tables_cell_coordinates:

            if is_image:
                # Convert the PIL Image to an OpenCV image (NumPy array)
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            else:
                image_cv = None

            # Sort boxes by ymin to separate rows
            boxes = sorted(boxes, key=lambda x: x['ymin'])

            # Calculate the average height of all boxes
            avg_height = np.mean([box['ymax'] - box['ymin'] for box in boxes])

            # Use a percentage (e.g., 10%) of the average height as the threshold for a new row
            threshold = self._threshold_percentage * avg_height

            # Identify unique rows by their y-coordinates
            rows = []
            last_ymin = None
            for box in boxes:
                ymin = box['ymin']
                if last_ymin is None or abs(ymin - last_ymin) > threshold:  # Adjust the threshold as needed
                    rows.append([])
                rows[-1].append(box)
                last_ymin = ymin

            # Sort each row by xmin to arrange columns
            for row in rows:
                row.sort(key=lambda x: x['xmin'])

            # Initialize an empty DataFrame
            df = pd.DataFrame()

            # Populate the DataFrame
            for row_idx, row_boxes in enumerate(rows):
                row_data = []
                for col_idx, box in enumerate(row_boxes):
                    text = self.get_text_from_page(page, box, image_cv)

                    row_data.append(text)

                # If it's the first row, set the DataFrame columns
                if row_idx == 0:
                    df = pd.DataFrame(columns=row_data)
                else:
                    df.loc[row_idx - 1] = row_data

            return df


