import PIL
from PIL import Image, ImageDraw
import fitz
from typing import Union, List
from layoutparser.models import Detectron2LayoutModel
from scanipy.elements import TextElement,TitleElement,ImageElement,TableElement,EquationElement


class LayoutDetector:
    """
    This class is responsible for parsing the layout of a document using a pre-trained Detectron2 model
    from LayoutParser python package.

    Source: https://github.com/Layout-Parser/layout-parser

    Attributes:
        model: The Detectron2 model for layout detection.
    """

    def __init__(self, device='cpu'):
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
    def __repr__(self):
        """
        Returns the official string representation of the LayoutDetector object.
        
        Returns:
            str: A string that can be used to recreate the LayoutDetector object.
        """
        return "LayoutDetector()"

    def __str__(self):
        """
        Returns a string representation of the LayoutDetector object, which is the same as its official representation.
        
        Returns:
            str: A string that can be used to recreate the LayoutDetector object.
        """
        return self.__repr__()

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

        # Getting image width and height 
        width, height = image.size
        
        # Iterate through each block in the DataFrame
        for _, block in layout.iterrows():
            # Extract coordinates of the bounding box
            x_min, y_min, x_max, y_max = block.x_1, block.y_1, block.x_2, block.y_2

            # Normalizing coordinates to be in range [0,1]
            x_min = x_min/width
            x_max = x_max/width
            y_min = y_min/height
            y_max = y_max/height
            
            # Use pattern matching to identify the type of the block and create the corresponding element
            element = None # Make sure that a new element is assigned
            match block.type:
                case "List": #TODO
                    element = TextElement(x_min, y_min, x_max, y_max, pipeline_step)
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

    # Debug Function
    def _draw_rectangle(self, image: Image.Image, x1: float, y1: float, x2: float, y2: float, 
                        outline_color: tuple = (255, 0, 0), thickness: int = 2) -> Image.Image:
        """
        Draw a rectangle on a PIL Image.

        Args:
            image (PIL.Image.Image): The input PIL Image.
            x1 (float): The x-coordinate of the top-left corner.
            y1 (float): The y-coordinate of the top-left corner.
            x2 (float): The x-coordinate of the bottom-right corner.
            y2 (float): The y-coordinate of the bottom-right corner.
            outline_color (tuple): The outline color as an RGB tuple (default is red).
            thickness (int): The outline thickness (default is 2).

        Returns:
            PIL.Image.Image: A new PIL Image with the rectangle drawn.
        """
        # Calculate PDF coordinates based on text element's normalized coordinates
        x1 = int(x1 * image.width)
        y1 = int(y1 * image.height)
        x2 = int(x2 * image.width)
        y2 = int(y2 * image.height)

        # Create a copy of the input image to avoid modifying the original
        image_copy = image.copy()
        
        # Create a drawing context on the copy of the image
        draw = ImageDraw.Draw(image_copy)

        # Draw the rectangle
        draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=thickness)

        return image_copy
