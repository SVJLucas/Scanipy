from .element import Element
import os

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
