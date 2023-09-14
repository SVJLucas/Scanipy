from transformers import pipeline
from cnstd import LayoutAnalyzer

class EquationFinder:
    """
    Locate equations within images using a fine-tuned Layout Analyzer model for equation detection.

    This model is a Mathematical Formula Detection (MFD) variant trained by Microsoft on the PubTables1M dataset.
    It is designed to detect equations in images.

    Source: https://github.com/breezedeus/cnstd

    Attributes:
        model (object): The loaded fine-tuned Table Transformer model for table detection.

    Example:
        >>> finder = EquationFinder()
        >>> detection_result = finder(image)
    """

    def __init__(self, use_cuda=False):
        """
        Initialize the EquationFinder class by loading the pre-trained model for equation detection.
        """
        device = 'gpu' if use_cuda else 'cpu'
        # Load the pre-trained Layout Analyzer from CNSTD
        self.model = LayoutAnalyzer(model_name='mfd',
                                    device=device)

    def __call__(self, image):
        """
        Detect equations in a given image using the pre-trained MFD model.

        Args:
            image: The image in which equation are to be detected.

        Returns:
            object: The detected equation information including bounding boxes and other attributes.
        """
        # Use the loaded model to detect equations in the given image
        return self.model(image)
