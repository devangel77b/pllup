#!/usr/bin/env python3

from abc import ABC, abstractmethod
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from book import Book
import logging





# for using Monospace font
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
FONT_DIR = "/usr/share/fonts/truetype/ubuntu"
UBUNTU_REGULAR_PATH = os.path.join(FONT_DIR,"UbuntuMono-R.ttf")
UBUNTU_BOLD_PATH = os.path.join(FONT_DIR,"UbuntuMono-B.ttf")

try:
    pdfmetrics.registerFont(TTFont("UbuntuMono", UBUNTU_REGULAR_PATH))
    pdfmetrics.registerFont(TTFont("UbuntuMono-Bold", UBUNTU_BOLD_PATH))
    DEFAULT_FONT = "UbuntuMono"
    logging.info("Successfully registered Ubuntu Monospace fonts.")
except Exception as e:
    logging.warning(f"Could not load Ubuntu Monospace from {FONT_DIR}: {e}. Falling back to Courier")
    DEFAULT_FONT = "Courier"



    


    
class BaseLabel(ABC):

    def __init__(self, width:float, height:float):
        self.width = width
        self.height = height
        
    @abstractmethod
    def draw(self, canvas_obj: Canvas, book:Book):
        pass


TITLE_SIZE = 7
BARCODE_TEXT_SIZE = 8
MARKER_FONT_SIZE = 8
CALL_SIZE = 10
EDGE_MARGIN = 2.5 * mm
    
class SpineLabel(BaseLabel):
    def __init__(self, width: float=30*mm, height: float=20*mm):
        super().__init__(width, height)

    def draw(self, canvas_obj: Canvas, book: Book):
        logging.info(f"Rendering spine label for {book.asset_id}")

        canvas_obj.saveState()
        canvas_obj.translate(self.width, 0)
        canvas_obj.rotate(90)
        v_width = self.height
        v_height = self.width
        
        display_title = book.title[:12].upper()
        t_width=canvas_obj.stringWidth(display_title, "Helvetica", TITLE_SIZE)
        canvas_obj.setFont("Helvetica", TITLE_SIZE)
        canvas_obj.drawString((v_width-t_width)/2, v_height-EDGE_MARGIN-TITLE_SIZE, display_title)

        canvas_obj.setFont("UbuntuMono", CALL_SIZE)
        
        # Stack lines from top to bottom, starting right below the title area
        # Leaving a safe margin down from the title line
        current_y = v_height - EDGE_MARGIN - TITLE_SIZE - CALL_SIZE - 2.0
        
        for line in book.call_number_lines:
            if current_y < EDGE_MARGIN:
                logging.warning(f"Call number for {book.asset_id} truncated due to label height.")
                break
            p_width = canvas_obj.stringWidth(line, "UbuntuMono", CALL_SIZE)
            canvas_obj.drawString((v_width - p_width) / 2, current_y, line)
            current_y -= (CALL_SIZE + 1.2)
            
        # 5. Restore the canvas coordinate landscape back to original configuration
        canvas_obj.restoreState()



class BarcodeLabel(BaseLabel):
    def __init__(self,  width: float=50*mm, height: float=30*mm):
        super().__init__(width,height)

    def draw(self, canvas_obj: Canvas, book:Book):
        canvas_obj.saveState()

        # vertical spacing
        title_y = self.height - EDGE_MARGIN - TITLE_SIZE
        marker_y = EDGE_MARGIN
        top_boundary = title_y - 1 * mm
        bottom_boundary = marker_y + MARKER_FONT_SIZE + 1 * mm
        barcode_height = 10 * mm
        available_height = top_boundary-bottom_boundary

        total_barcode_footprint = barcode_height + BARCODE_TEXT_SIZE
        pocket_center_y = bottom_boundary + (available_height/2.0)
        start_y = (pocket_center_y - (total_barcode_footprint / 2.0)) + BARCODE_TEXT_SIZE
        
        short_title = book.title[:32].upper()
        canvas_obj.setFont("Helvetica-Bold", 7)
        canvas_obj.drawCentredString(self.width / 2.0, title_y, short_title)

        # 2. Middle Section: Code 128 Barcode Layout
        # Turning on humanReadable means ReportLab natively prints the barcode string text below the bars.
        barcode = code128.Code128(
            str(book.asset_id),
            barWidth=0.375 * mm,
            barHeight=barcode_height,
            quiet=True,
            humanReadable=True,
            fontName="UbuntuMono",
            fontSize=8
        )
        
        # Calculate start position to center the barcode graphic across the 50mm roll width
        barcode_width = barcode.width
        start_x = (self.width - barcode_width) / 2.0

        # Draw barcode in the center vertical region
        barcode.drawOn(canvas_obj, start_x, start_y)

        # 3. Bottom Section: Centered "S&E library" institutional marker text
        canvas_obj.setFont("Helvetica-Bold", MARKER_FONT_SIZE)
        canvas_obj.drawCentredString(self.width / 2.0, marker_y, "S&E LIBRARY")
        
        canvas_obj.restoreState()
    
