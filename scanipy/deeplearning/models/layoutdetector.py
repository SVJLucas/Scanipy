import PIL
from typing import Union, List
from layoutparser.models import Detectron2LayoutModel
from scanipy.elements import TextElement,TitleElement,ImageElement,TableElement


class LayoutDetector:
    """
    This class is responsible for parsing the layout of a document using a pre-trained Detectron2 model
    from LayoutParser python package.

    Source: https://github.com/Layout-Parser/layout-parser

    Attributes:
        model: The Detectron2 model for layout detection.
    """

    def __init__(self, device):
        """
        Initializes the LayoutDetector class with a given device.
        
        Args:
            device: The device on which the Detectron2 model will run.
        """
        # Verify the type of the device argument
        if not isinstance(device, str):
            raise TypeError("Device must be a string.")
        
        # Initialize the Detectron2 model with specific configurations and label mapping
        self.model = Detectron2LayoutModel(
            'lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
            label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
            device=device
        )

    def __call__(self, image: PIL.Image, pipeline_step: Union[int, None] = None) -> List[Union[TextElement, TitleElement, ImageElement, TableElement]]:
        """
        Detects layout elements in the given image and returns them as a list.
        
        Args:
            image: The image in which to detect layout elements.
            pipeline_step: An optional integer representing the step in a pipeline. Defaults to None.
        
        Returns:
            empty_elements: A list of detected layout elements, but only with its positions (no extracted content yet).
        """
        # Verify the type of the image argument
        if not isinstance(image, PIL.Image.Image):
            raise TypeError("Image must be a PIL.Image object.")
        
        # Verify the type of the pipeline_step argument
        if not (isinstance(pipeline_step, int) or pipeline_step is None):
            raise TypeError("pipeline_step must be an integer or None.")
        
        # Perform layout detection on the image and convert the result to a DataFrame
        layout = self.model.detect(image).to_dataframe()
        
        # Initialize an empty list to store detected elements
        elements = []
        
        # Iterate through each block in the DataFrame
        for _, block in layout.iterrows():
            # Extract coordinates of the bounding box
            x_min, y_min, x_max, y_max = block.x_1, block.y_1, block.x_2, block.y_2
            
            # Use pattern matching to identify the type of the block and create the corresponding element
            match block.type:
                case "Text":
                    element = TextElement(x_min, y_min, x_max, y_max, pipeline_step)
                case "Title":
                    element = TitleElement(x_min, y_min, x_max, y_max, pipeline_step)
                case "Figure":
                    element = ImageElement(x_min, y_min, x_max, y_max, pipeline_step)
                case "Table":
                    element = TableElement(x_min, y_min, x_max, y_max, pipeline_step)
            
            # Append the detected element to the list
            elements.append(element)
        
        # Return the list of detected elements
        return elements


