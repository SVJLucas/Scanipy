from scanipy.elements import EquationElement
import pdf2image
from pix2text import Pix2Text, merge_line_texts

DPI = 200
IMAGE_TO_FITZ_CONSTANT = 72 / DPI

class EquationExtractor:
    def __init__(self):
        self.model = Pix2Text(analyzer_config=dict(model_name='mfd'))

    def extract(self, path, document, pipeline_step):
        imgs = pdf2image.convert_from_path(path)
        for page, image in enumerate(imgs):
            outs = self.model(image, resized_shape=600)
            isolated_equations = [o for o in outs if o['type'] == 'isolated']
            for eq in isolated_equations:
                x0, y0 = eq['position'][0]
                x2, y2 = eq['position'][2]
                equation = EquationElement(x0, y0, x2, y2,
                                           pipeline_step=pipeline_step, latex_content=eq['text'], is_inside_text=False)
                isolated_check = True
                for element in document.elements.get(page, []):
                    if equation.is_in(element):
                        isolated_check = False
                        break
                if isolated_check:
                    document.add_element(page, equation)
