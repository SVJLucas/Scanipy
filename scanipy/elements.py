import os


class Element:
    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step = None):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.pipeline_step = pipeline_step
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2


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


class TableElement(Element):
    """
    Represents a table element for printing tabular data.

    Attributes:
    df (pandas.DataFrame): The DataFrame containing tabular data.

    Methods:
    print(output_folder):
        Returns the formatted table for printing to an output folder.

    """

    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step, df):
        """
        Initializes a new TableElement.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing tabular data.
        """
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)
        self.df = df

    def print(self, output_folder):
        """
        Generates the formatted table for printing.

        Parameters:
        output_folder (str): The path to the output folder.

        Returns:
        str: The formatted table.
        """
        response = self.df.to_markdown() + '\n\n'
        return response


class ImageElement(Element):
    """
    Represents an image element within a document.

    Attributes:
        key (str): A unique key for the image element.
        content: The image content.
        image_ext (str): The file extension for the image (e.g., 'jpg', 'png').
    """

    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step, key, content, image_ext):
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)
        self.key = key
        self.content = content
        self.image_ext = image_ext

    def print(self, output_folder):
        """
        Print the image element to the document and save the image to a file.

        :param output_folder: The folder where the image file will be saved.
        :return: Markdown representation of the image element.
        """
        filename = f"{self.key}.{self.image_ext}"
        output_path = os.path.join(output_folder, filename)
        self.content.save(open(output_path, "wb"))
        return f"\n![image]({filename})\n\n"
