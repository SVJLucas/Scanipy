import PIL
from typing import Union, List
from cnstd import LayoutAnalyzer
from .elements import EquationElement

class EquationFinder:
    """
    Locate equations within images using a fine-tuned Layout Analyzer model for equation detection.

    This is a chinese Mathematical Formula Detection (MFD) YoloV7 trained in the IBEM dataset (english) and the CnMFD_Dataset (chinese).
    
    Source: https://github.com/breezedeus/cnstd

    Attributes:
        model (object): The loaded YoloV7 for table detection.

    Example:
        >>> finder = EquationFinder()
        >>> detection_result = finder(image)
    """

    def __init__(self, device):
        """
        Initialize the EquationFinder class by loading the pre-trained model for equation detection.
        Args:
            device: The device on which the Yolov7 model will run.
        """

        # Verify the type of the device argument
        if not isinstance(device, str):
            raise TypeError("Device must be a string.")
          
        # Load the pre-trained Layout Analyzer from CNSTD
        self.model = LayoutAnalyzer(model_name='mfd',
                                    device=device)

    def __call__(self, image: PIL.Image, pipeline_step: Union[int, None] = None) -> List[EquationElement]:
        """
        Detects equation elements in the given image and returns them as a list.
        
        Args:
            image (PIL.Image): The image in which to detect layout elements.
            pipeline_step (int or None): An optional integer representing the step in a pipeline. Defaults to None.
        
        Returns:
            empty_elements (List[EquationElement]): A list of detected layout elements, but only with its positions (no extracted content yet).
        """
        # Use the loaded model to detect equations in the given image
        equations = self.model(image)
        empty_elements = []
        for equation in equations:
          
          # Getting position values
          x_min, y_min = equation['box'][:,0]
          x_max, y_max = equation['box'][:,3]

          # Normalizing Coordinates
          x_min /= image.size[0]
          y_min /= image.size[1]
          x_max /= image.size[0]
          y_max /= image.size[1]

          # Verifying if the equation is in the middle of  text
          is_inside_text = bool(equation['type']=='embedding')

          # Creating element
          element = EquationElement(x_min, y_min, x_max, y_max, pipeline_step, is_inside_text = is_inside_text)

          # Adding EquationElement in the list
          empty_elements.append(element)
          
        return empty_elements
