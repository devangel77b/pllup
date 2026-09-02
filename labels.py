#!/usr/bin/env python3

from abc import ABC, abstractmethod
from reportlab.graphics.barcode import code128
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
    #pdfmetrics.registerFont(TTFont("UbuntuMono-Bold", UBUNTU_BOLD_PATH))
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
CALL_SIZE = 10
EDGE_MARGIN = 2.5 * mm
    
class SpineLabel(BaseLabel):
    def __init__(self, width: float=30*mm, height: float=20*mm):
        super().__init__(width, height)
        self.font = DEFAULT_FONT

    def draw(self, canvas_obj: Canvas, book: Book):
        logging.info(f"Rendering spine label for {book.asset_id}")

        canvas_obj.saveState()
        canvas_obj.translate(self.width, 0)
        canvas_obj.rotate(90)
        v_width = self.height
        v_height = self.width
        
        display_title = book.title[:12].upper()
        t_width=canvas_obj.stringWidth(display_title, self.font, TITLE_SIZE)
        canvas_obj.setFont(self.font, TITLE_SIZE)
        canvas_obj.drawString((v_width-t_width)/2, v_height-EDGE_MARGIN-TITLE_SIZE, display_title)

        call_parts = book.call_number.split()
        canvas_obj.setFont(self.font, CALL_SIZE)
        
        # Stack lines from top to bottom, starting right below the title area
        # Leaving a safe margin down from the title line
        current_y = v_height - EDGE_MARGIN - TITLE_SIZE - CALL_SIZE - 2.0
        
        for part in call_parts:
            p_width = canvas_obj.stringWidth(part, self.font, CALL_SIZE)
            # Centers each part across the 20mm virtual width
            canvas_obj.drawString((v_width - p_width) / 2, current_y, part)
            current_y -= (CALL_SIZE + 1.5)  # Move down for the next line stack
            
        # 5. Restore the canvas coordinate landscape back to original configuration
        canvas_obj.restoreState()
