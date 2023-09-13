import os

class TextElement:
    """
    Represents a text element with optional styling.

    Attributes:
    content (str): The content of the text element.
    style (str, optional): The style of the text element, e.g., 'title'.

    Methods:
    print(output_folder):
        Returns the formatted text for printing to an output folder.

    """

    def __init__(self, content, style=None):
        """
        Initializes a new TextElement.

        Parameters:
        content (str): The content of the text element.
        style (str, optional): The style of the text element, e.g., 'title'.
        """
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

class TableElement:
    """
    Represents a table element for printing tabular data.

    Attributes:
    df (pandas.DataFrame): The DataFrame containing tabular data.

    Methods:
    print(output_folder):
        Returns the formatted table for printing to an output folder.

    """

    def __init__(self, df):
        """
        Initializes a new TableElement.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing tabular data.
        """
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

class ImageElement:
    """
    Represents an image element within a document.

    Attributes:
        key (str): A unique key for the image element.
        content: The image content.
        image_ext (str): The file extension for the image (e.g., 'jpg', 'png').
    """

    def __init__(self, key, content, image_ext):
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
