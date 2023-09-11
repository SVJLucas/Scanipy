import pickle
from pix2tex.cli import LatexOCR
from constats.paths import PATH_TO_IMAGE_TO_LATEX_MODEL


class ImageToLatex:
    """
    Convert images of mathematical formulas to LaTeX code using the pix2tex model.

    This model utilizes a Vision Transformer (ViT) encoder with a ResNet backbone and a Transformer decoder.
    It is specifically designed to convert images of mathematical formulas into their corresponding LaTeX code.

    Source: https://github.com/lukas-blecher/LaTeX-OCR

    Attributes:
        model (object): The loaded pix2tex model for LaTeX OCR.

    Example:
        >>> img_to_latex = ImageToLatex()
        >>> latex_code = img_to_latex(image)
    """

    def __init__(self):
        """
        Initialize the ImageToLatex class by loading the pre-trained pix2tex model.
        """
        # Load the pre-trained pix2tex model from a pickle file
        self.model = pickle.load(open(PATH_TO_IMAGE_TO_LATEX_MODEL, 'rb'))

    def __call__(self, image):
        """
        Convert an image containing a mathematical formula to LaTeX code using the pre-trained pix2tex model.

        Args:
            image (PIL.Image): The image that contains a mathematical formula.

        Returns:
            str: The LaTeX code corresponding to the mathematical formula in the image.
        """
        # Use the loaded model to convert the image into LaTeX code
        return self.model(image)
