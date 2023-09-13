from .element import Element
class TextElement(Element):
    """
    Represents a text element with optional styling.

    Attributes:
    content (str): The content of the text element.
    style (str, optional): The style of the text element, e.g., 'title'.

    Methods:
    print(output_folder):
        Returns the formatted text for printing to an output folder.

    """

    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step, content, style=None):
        """
        Initializes a new TextElement.

        Parameters:
        content (str): The content of the text element.
        style (str, optional): The style of the text element, e.g., 'title'.
        """
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)
        self.content = content
        self.style = style

    def print(self, output_folder):
        """
        Generates the formatted text for printing.

        Parameters:
        output_folder (str): The path to the output folder.

        Returns:
        str: The formatted text.
        """
        response = self.content + '\n\n'
        if self.style == 'title':
            response = '## ' + response
        return response


