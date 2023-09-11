'''
This file contains the implementation of TableStructureAnalyzer class

Created by:
    Lucas José (lucas.jose.veloso.de.souza@gmail.com)
    Date: September 11, 2023
'''

import pickle
from transformers import pipeline


class TableFinder:
    """
    Locate tables within images using a fine-tuned Table Transformer model for table detection.

    This model is a Table Transformer (DETR) variant trained by Microsoft on the PubTables1M dataset.
    It is designed to detect tables in images.

    Source: https://github.com/microsoft/table-transformer

    Attributes:
        model (object): The loaded fine-tuned Table Transformer model for table detection.

    Example:
        >>> finder = TableFinder()
        >>> detection_result = finder(image)
    """

    def __init__(self):
        """
        Initialize the TableFinder class by loading the pre-trained model for table detection.
        """
        # Load the pre-trained Table Transformer model from a pickle file for table detection
        self.model = pipeline("object-detection", model="microsoft/table-transformer-detection")

    def __call__(self, image):
        """
        Detect tables in a given image using the pre-trained Table Transformer model.

        Args:
            image: The image in which tables are to be detected.

        Returns:
            object: The detected table information including bounding boxes and other attributes.
        """
        # Use the loaded model to detect tables in the given image
        return self.model(image)
