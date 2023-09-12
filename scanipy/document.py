import os
import layoutparser as lp

class Document:
    """
    Represents a document containing various elements, such as images.

    Attributes:
        elements (list): A list of elements in the document.
    """

    def __init__(self):
        self.elements = []
        self.images = []
        self.layouts = []

    def to_markdown(self, output_folder, filename='output.md'):
        """
        Generate a Markdown document from the elements and save it to a file.

        :param output_folder: The folder where the Markdown file will be saved.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output = ""
        for element in self.elements:
            element_output = element.print(output_folder)
            output += element_output
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w') as f:
            f.write(output)

    def add_image(self, content, image_ext):
        """
        Add an image element to the document.

        :param content: The image content to be added.
        :param image_ext: The file extension for the image (e.g., 'jpg', 'png').
        """
        image = ImageElement(f'img{len(self.elements)}', content, image_ext)
        self.elements.append(image)

    def add_text(self, content, style=None):
        text = TextElement(content, style)
        self.elements.append(text)

    def visualize_layout(self, page=0):
        return lp.draw_box(self.images[page], self.layouts[page], box_width=5, box_alpha=0.2)

    def store_page(self, image, layout):
        self.layouts.append(layout)
        self.images.append(image)

class TextElement:
    def __init__(self, content, style=None):
        self.content = content
        self.style = style

    def print(self, output_folder):
        response = self.content + '\n\n'
        if self.style == 'title':
            response = '## ' + response
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