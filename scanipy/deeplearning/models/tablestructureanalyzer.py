'''
This file contains the implementation of TableStructureAnalyzer class

Created by:
    Lucas José (lucas.jose.veloso.de.souza@gmail.com)
    Date: September 11, 2023
'''


import pickle
from transformers import pipeline


class TableStructureAnalyzer:
    """
    Analyze the structure of tables in images using a fine-tuned Table Transformer model.

    The model is based on the Table Transformer (DETR) by Microsoft, trained on PubTables1M.
    It can detect structural elements like rows and columns within tables in images.

    Source: https://github.com/microsoft/table-transformer

    Attributes:
        model (object): The loaded fine-tuned Table Transformer model.

    Example:
        >>> analyzer = TableStructureAnalyzer()
        >>> result = analyzer(image)
    """

    def __init__(self):
        """
        Initialize the TableStructureAnalyzer by loading the pre-trained model.
        """
        # Load the fine-tuned Table Transformer model from a pickle file
        self.model = pipeline("object-detection", model="microsoft/table-transformer-structure-recognition")

    def __call__(self, image):
        """
        Analyze the table structure in a given image.

        Args:
            image: The image containing the table to be analyzed.

        Returns:
            object: The analyzed table structure, including elements like rows and columns.
        """
        # Use the loaded model to analyze the table structure in the given image
        return self.model(image)
