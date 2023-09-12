import pdf2image
import layoutparser as lp
import numpy as np
import PIL

PIL.Image.LINEAR = PIL.Image.BILINEAR
def is_valid_utf8(s):
    try:
        s.encode('utf-8').decode('utf-8')
        return True
    except UnicodeEncodeError:
        return False


class TextExtractor:
    def __init__(self, filepath):
        self.model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                              extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                              label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})
        self.ocr_agent = lp.TesseractAgent(languages='eng')
        self.images = []
        self.layouts = []

        imgs = pdf2image.convert_from_path(filepath)
        for img in imgs:
            array_img = np.asarray(img)
            layout = self.model.detect(array_img)
            self.images.append(array_img)
            self.layouts.append(layout)

    def extract(self, document):
        for i, img in enumerate(self.images):
            image_width = len(img[0])
            layout = self.layouts[i]
            text_blocks = lp.Layout([b for b in layout if b.type == 'Text' or b.type == 'Title'])

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

                # Perform OCR
                text = self.ocr_agent.detect(segment_image)

                # Save OCR result
                block.set(text=text, inplace=True)
            for txt in text_blocks:
                content = txt.text.strip()
                style = None
                if txt.type == 'Title':
                    style = 'title'
                document.add_text(content, style)

    def plot(self, page_number):
        lp.draw_box(self.images[page_number], self.layouts[page_number], box_width=5, box_alpha=0.2)
