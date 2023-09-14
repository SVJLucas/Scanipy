import PIL
from layoutparser.models import Detectron2LayoutModel
from elements import TextElement,TitleElement,ImageElement,TableElement


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

    def __call__(self, image: PIL.Image) -> List[Union[TextElement, TitleElement, ImageElement, TableElement]]:
        """
        Detects layout elements in the given image and returns them as a list.
        
        Args:
            image: The image in which to detect layout elements.
            
        Returns:
            elements: A list of detected layout elements.
        """
        # Verify the type of the image argument
        if not isinstance(image, PIL.Image.Image):
            raise TypeError("Image must be a PIL.Image object.")
        
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
                    element = TextElement(x_min, y_min, x_max, y_max)
                case "Title":
                    element = TitleElement(x_min, y_min, x_max, y_max)
                case "Figure":
                    element = ImageElement(x_min, y_min, x_max, y_max)
                case "Table":
                    element = TableElement(x_min, y_min, x_max, y_max)
            
            # Append the detected element to the list
            elements.append(element)
        
        # Return the list of detected elements
        return elements

