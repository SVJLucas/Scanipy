import pickle
from pix2tex.cli import LatexOCR


class EquationToLatex:
    """
    Convert images of mathematical formulas to LaTeX code using the pix2tex model.

    This model utilizes a Vision Transformer (ViT) encoder with a ResNet backbone and a Transformer decoder.
    It is specifically designed to convert images of mathematical formulas into their corresponding LaTeX code.

    Source: https://github.com/lukas-blecher/LaTeX-OCR

    Attributes:
        model (object): The loaded pix2tex model for LaTeX OCR.

    Example:
        >>> equation_to_latex = EquationToLatex()
        >>> image = Image.open('equation_image.png')
        >>> latex_code = equation_to_latex(image)
    """

    def __init__(self):
        """
        Initialize the EquationToLatex class by loading the pre-trained pix2tex model.
        """
        # Load the pre-trained pix2tex model from a pickle file
        self.model = LatexOCR()

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
    def __repr__(self):
        """
        Returns the official string representation of the EquationToLatex object.
        
        Returns:
            str: A string that can be used to recreate the EquationToLatex object.
        """
        return "EquationToLatex()"

    def __str__(self):
        """
        Returns a string representation of the EquationToLatex object, which is the same as its official representation.
        
        Returns:
            str: A string that can be used to recreate the EquationToLatex object.
        """
        return self.__repr__()
