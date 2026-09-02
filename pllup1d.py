#!/usr/bin/env python

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128

if __name__ == "__main__":

    width = 50 * mm
    height = 30 * mm
    c = canvas.Canvas("stub3.pdf",pagesize=(width, height))
    
    # test spine label with bar code
    c.setFont("Helvetica-Bold", 9)
    c.drawString(4 * mm, 24 * mm, "THE HOBBIT")
    book_id = "B00001"
    bc = code128.Code128(book_id, barHeight=10 * mm, barWidth=0.3 * mm)
    bc.drawOn(c, 4 * mm, 9 * mm)
    c.setFont("Courier-Bold", 14)
    c.drawString(5 * mm, 4 * mm, "FIC TOL")
    c.showPage()

    c.save()
    
