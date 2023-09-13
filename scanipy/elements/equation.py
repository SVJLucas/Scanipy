from .element import Element


class EquationElement(Element):
    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step, latex_content, is_inside_text=False):
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)
        self.latex_content = latex_content
        self.is_inside_text = is_inside_text

    def print(self, output_folder):
        return self.latex_content + '\n\n'
