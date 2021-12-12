import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import cv2
import io
import math
import os
import pdfplumber
import tempfile
from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader, PdfFileWriter


def convert_page_to_img(pdf_fpath, img_fpath, pageno=0):
    
    resolution = 300
    inputpdf = PdfFileReader(open(pdf_fpath, 'rb'))

    dst_pdf = PdfFileWriter()
    dst_pdf.addPage(inputpdf.getPage(pageno))
    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    img = Image(file=pdf_bytes, resolution=resolution)
    img.background_color = Color("white")
    img.alpha_channel = 'remove'
    img.convert('jpeg')
    img.save(filename=img_fpath)

    imgsize = img.size

    return img_fpath, imgsize


def get_bounding_boxes(fpath):

    img = cv2.imread(fpath)
    imgh, imgw = img.shape[:2]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

    # Get rectanges
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    bounds = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)

        x0 = x
        y0 = y
        x1 = x + w
        y1 = y + h

        x0 = x0 / float(imgw)
        y0 = y0 / float(imgh)
        x1 = x1 / float(imgw)
        y1 = y1 / float(imgh)

        bounds.append((float(x0), float(y0), float(x1), float(y1)))

    return bounds


def convert_opencv_bbox_to_pdfplumber(bbox, pagewidth, pageheight):

    x0, y0, x1, y1 = bbox
    x0 = math.floor(x0 * pagewidth)
    y0 = math.floor(y0 * pageheight)
    x1 = math.ceil(x1 * pagewidth)
    y1 = math.ceil(y1 * pageheight)

    return (x0, y0, x1, y1)


def get_text_in_bbox(pdf_fpath, pageno, bbox):

    with pdfplumber.open(pdf_fpath) as pdf:
        page = pdf.pages[pageno]
        page_cropped = page.crop(bbox)
        text = page_cropped.extract_text()

        return text


def clean_text(text):

    text = text.replace('\n', ' ').strip()
    return text


def parse_overview_info(pdf_fpath):
    
    with pdfplumber.open(pdf_fpath) as pdf:
        first_page = pdf.pages[0]

    pagewidth = float(first_page.width)
    pageheight = float(first_page.height)

    with tempfile.TemporaryDirectory() as tmpdirname:
        img_fpath = os.path.join(tmpdirname, 'GA-pag0.jpeg')
        _, imgsize = convert_page_to_img(pdf_fpath, img_fpath)

        bboxes = get_bounding_boxes(img_fpath)

        print(imgsize, len(bboxes))

        result = []
        for bbox in bboxes:
            bbox = convert_opencv_bbox_to_pdfplumber(bbox, pagewidth, pageheight)
            bbox_text = get_text_in_bbox(pdf_fpath, pageno=0, bbox=bbox)
            
            if bbox_text is not None:
                bbox_text = clean_text(bbox_text)
                result.append(bbox_text)

    return result
