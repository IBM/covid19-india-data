from wand.image import Image
import io
import os
import tempfile
import math

from PyPDF2 import PdfFileWriter, PdfFileReader
from mmdet.apis import init_detector, inference_detector, show_result_pyplot


class ExtractTable(object):
    """
    Utilizes CascadeTabNet (https://github.com/DevashishPrasad/CascadeTabNet) to detect table boundaries
    These table boundaries are then used by pdf table extraction libraries to extract table from
    specific regions that they would've otherwise missed.
    """
    
    def __init__(self, pdf_fpath, pagenums=None, resolution=200, 
                threshold=0.85, model_device='cpu', stretch_bounds=0.05,
                origin='top-left'):
        
        self.pdf_fpath = pdf_fpath
        self.pagenums = pagenums
        self.resolution = resolution
        self.threshold = threshold
        self.model_device = model_device
        self.stretch_bounds = stretch_bounds
        self.origin = origin

        self.load_model()

    def load_model(self):

        self._config_fpath = os.environ['TABNET_CONFIGPATH']
        self._model_fpath = os.environ['TABNET_MODELPATH']
        self._model = init_detector(self._config_fpath, self._model_fpath, device=self.model_device)

    def convert_pdf2imgs(self, dirname):

        inputpdf = PdfFileReader(open(self.pdf_fpath, 'rb'))
        pages = list(range(inputpdf.numPages)) if self.pagenums is None else self.pagenums
        imgpaths = {}

        for pagenum in pages:
            fname = os.path.join(dirname, f'pdfimg-{pagenum}.jpeg')

            dst_pdf = PdfFileWriter()
            dst_pdf.addPage(inputpdf.getPage(pagenum))
            pdf_bytes = io.BytesIO()
            dst_pdf.write(pdf_bytes)
            pdf_bytes.seek(0)

            img = Image(file=pdf_bytes, resolution=self.resolution)
            img.convert('jpeg')
            img.save(filename=fname)

            imgsize = img.size

            imgpaths[pagenum] = {'fpath': fname, 'shape': imgsize}

        return imgpaths

    def get_page_props(self, pagenum):

        inputpdf = PdfFileReader(open(self.pdf_fpath, 'rb'))
        dims = inputpdf.getPage(pagenum).mediaBox
        _, _, width, height = dims
        return float(width), float(height)

    def unnormalize_boundaries(self, boundaries, width, height):

        coords = []
        for boundary in boundaries:
            x1, y1, x2, y2 = boundary
            x1 = math.floor(x1 * width)
            y1 = math.floor(y1 * height)
            x2 = math.ceil(x2 * width)
            y2 = math.ceil(y2 * height)
            coords.append((x1, y1, x2, y2))

        return coords


    def correct_for_origin(self, coords, width, height):
        """
        Computed coordinates from the model assumes "top-left"
        as the origin. Some libraries though define "bottom-left"
        as the origin, and therefore, this method corrects the 
        computed coordinates
        """

        result = []
        for coordinate in coords:
            x1, y1, x2, y2 = coordinate

            if self.origin == 'top-left':
                pass        # do nothing since the model has the same origin
            elif self.origin == 'bottom-left':
                y1 = height - y1
                y2 = height - y2
            elif self.origin == 'top-right':
                x1 = width - x1
                x2 = width - x2
            elif self.origin == 'bottom-right':
                x1 = width - x1
                x2 = width - x2
                y1 = height - y1
                y2 = height - y2
            else:
                raise AttributeError('origin can only be [top-left, top-right, bottom-left, bottom-right]')
            
            result.append((x1, y1, x2, y2))

        return result

    
    def get_table_boundaries(self, fpath, imgsize):

        def get_table_coords(tblarray, width, height):

            tables = []

            for tbl in tblarray:
                x1, y1, x2, y2, conf = tbl

                if conf < self.threshold:
                    continue
                    
                # normalize coords
                x1 = x1 / float(width)
                y1 = y1 / float(height)
                x2 = x2 / float(width)
                y2 = y2 / float(height)

                tables.append((x1, y1, x2, y2))

            return tables

        result = inference_detector(self._model, fpath)
        width, height = imgsize

        tables = []

        tables.extend(get_table_coords(result[0][0], width, height))    # Get bordered tables
        tables.extend(get_table_coords(result[0][2], width, height))    # Get unbordered tables

        return tables

    def stretch_boundaries(self, boundaries, width, height):

        result = []
        for boundary in boundaries:
            x1, y1, x2, y2 = boundary

            box_w = x2 - x1
            box_h = y2 - y1

            x1 = max(0, x1 - math.floor(self.stretch_bounds * box_w))
            y1 = max(0, y1 - math.floor(self.stretch_bounds * box_h))
            x2 = min(width, math.ceil(x2 + self.stretch_bounds * box_w))
            y2 = min(height, math.ceil(y2 + self.stretch_bounds * box_h))

            result.append((x1, y1, x2, y2))

        return result

    def extract(self):

        tables = {}         # pagenum -> table coordinates dictionary

        with tempfile.TemporaryDirectory() as tmpdirname:
            
            imgpaths = self.convert_pdf2imgs(tmpdirname)

            for pagenum in sorted(imgpaths.keys()):
                val = imgpaths[pagenum]
                fpath = val['fpath']
                imgshape = val['shape']

                table_boundaries = self.get_table_boundaries(fpath, imgshape)                       # normalized boundaries
                width, height = self.get_page_props(pagenum)                                        # shape of PDF
                table_boundaries = self.unnormalize_boundaries(table_boundaries, width, height)     # boundaries in the PDF space
                table_boundaries = self.stretch_boundaries(table_boundaries, width, height)
                table_boundaries = self.correct_for_origin(table_boundaries, width, height)

                tables[pagenum] = table_boundaries
        
        return tables
