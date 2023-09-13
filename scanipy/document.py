import os
import layoutparser as lp
import numpy as np
from .elements import TableElement, TextElement, ImageElement
import matplotlib.pyplot as plt


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
        self.table_extractor_data = []

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

    def add_element(self, element):
        self.elements.append(element)

    def visualize_pipeline(self, page=0, step=0):
        if step == 0:
            return lp.draw_box(self.images[page], self.layouts[page], box_width=5, box_alpha=0.2)
        if step == 1:
            self._visualize_tables(self.table_extractor_data[page]['image'],
                                   self.table_extractor_data[page]['detected_tables'])
            return
        raise ValueError(f'step {step} not recognized')

    def visualize_block(self, page=0, block=0):
        block = self.layouts[page][block]
        segment_image = (block
                         .pad(left=5, right=15, top=5, bottom=5)
                         .crop_image(np.asarray(self.images[page])))
        return block

    def _visualize_tables(self, image, detected_tables):
        # Create a matplotlib figure and axis for visualization
        fig, ax = plt.subplots(1)
        # Display the RGB image
        ax.imshow(image)

        # Loop through each detected table to draw its bounding box
        for table in detected_tables:
            xmin, ymin, xmax, ymax = table['box'].values()

            # Create a red rectangle around the table
            rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='r', facecolor='none')

            # Add the rectangle to the plot
            ax.add_patch(rect)

            # Add label and confidence score
            label = f"{table['label']} ({table['score']:.2f})"
            plt.text(xmin, ymin, label, color='white', fontsize=12, bbox=dict(facecolor='red', alpha=0.5))

        # Hide axes and show the plot
        plt.axis('off')
        plt.show()

    def store_page(self, image, layout):
        self.layouts.append(layout)
        self.images.append(image)

    def save_tables(self, image, detected_tables):
        self.table_extractor_data.append({'image': image, 'detected_tables': detected_tables})
