from scanipy.elements import EquationElement
import pdf2image
from cnstd import LayoutAnalyzer
from pix2tex.cli import LatexOCR
import matplotlib.pyplot as plt
import numpy as np
DPI = 200
IMAGE_TO_FITZ_CONSTANT = 72 / DPI
import PIL
class EquationExtractor:
    def __init__(self):
        # self.model = Pix2Text(analyzer_config=dict(model_name='mfd'))

        self.model = LayoutAnalyzer(model_name='mfd',
                                    device='cuda:0')
        self.extractor_model = LatexOCR()

    def extract(self, path, document, pipeline_step):
        imgs = pdf2image.convert_from_path(path)
        for page, image in enumerate(imgs):
            outs = self.model(image, resized_shape=600)
            isolated_equations = [o for o in outs if o['type'] == 'isolated']
            for eq in isolated_equations:
                x0, y0 = eq['box'][0, :]
                x2, y2 = eq['box'][2, :]
                segment_image = PIL.Image.fromarray(np.asarray(image)[int(y0):int(y2), int(x0):int(x2)])
                latex_content = self.extractor_model(segment_image)
                latex_content = f'$$\n{latex_content}\n$$'
                equation = EquationElement(x0, y0, x2, y2,
                                           pipeline_step=pipeline_step, latex_content=latex_content, is_inside_text=False)
                isolated_check = True
                for element in document.elements.get(page, []):
                    if equation.is_in(element):
                        isolated_check = False
                        break
                if isolated_check:
                    document.add_element(page, equation)
