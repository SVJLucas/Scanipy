import pdf2image
import layoutparser as lp
import numpy as np
import PIL
from doctr.models import ocr_predictor
import torch
import matplotlib.pyplot as plt

PIL.Image.LINEAR = PIL.Image.BILINEAR


def is_valid_utf8(s):
    try:
        s.encode('utf-8').decode('utf-8')
        return True
    except UnicodeEncodeError:
        return False


class TextExtractor:
    def __init__(self):
        # models available at https://layout-parser.readthedocs.io/en/latest/notes/modelzoo.html

        self.tesseract_ocr = lp.TesseractAgent(languages='eng')
        self.doctr_ocr = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_mobilenet_v3_small', pretrained=True)
        device = "cpu"
        if torch.cuda.is_available():
            self.doctr_ocr.cuda()
            device = "cuda:0"

        self.model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                              extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                              label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
                                              device=device)

    def extract_tesseract(self, segment_image):
        return self.tesseract_ocr.detect(segment_image)

    def extract_doctr(self, segment_image):
        out = self.doctr_ocr([segment_image])
        text = []
        json = out.export()

        for block in json['pages'][0]['blocks']:
            for line in block['lines']:
                for word in line['words']:
                    text.append(word['value'])
        return ' '.join(text)

    def extract(self, filepath, document):
        images = []
        layouts = []

        imgs = pdf2image.convert_from_path(filepath)
        for img in imgs:
            array_img = np.asarray(img)
            layout = self.model.detect(array_img)
            images.append(array_img)
            layouts.append(layout)
            document.store_page(img, layout)

        for i, img in enumerate(images):
            image_width = len(img[0])
            text_blocks = layouts[i]

            # Sort element ID of the left column based on y1 coordinate
            left_interval = lp.Interval(0, image_width / 2, axis='x').put_on_canvas(img)
            left_blocks = text_blocks.filter_by(left_interval, center=True)._blocks
            left_blocks.sort(key=lambda b: b.coordinates[1])

            # Sort element ID of the right column based on y1 coordinate
            right_blocks = [b for b in text_blocks if b not in left_blocks]
            right_blocks.sort(key=lambda b: b.coordinates[1])

            # Sort the overall element ID starts from left column
            text_blocks = lp.Layout([b.set(id=idx) for idx, b in enumerate(left_blocks + right_blocks)])

            for block in text_blocks:
                # Crop image around the detected layout
                segment_image = (block
                                 .pad(left=5, right=15, top=5, bottom=5)
                                 .crop_image(img))

                if block.type in ['Text', 'Title']:
                    # Perform OCR
                    text = self.extract_doctr(segment_image)
                    text = text.strip()
                    style = None
                    if block.type == 'Title':
                        style = 'title'
                    document.add_text(text, style)
                elif block.type == 'Figure':
                    content = PIL.Image.fromarray(segment_image)
                    document.add_image(content, 'png')

    def plot(self, page_number):
        lp.draw_box(images[page_number], layouts[page_number], box_width=5, box_alpha=0.2)
