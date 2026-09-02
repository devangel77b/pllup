#!/usr/bin/env python3

import logging
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Direct dependencies from our step 6 architecture
from book import Book
from labels import BaseLabel






def generate_continuous_label_stream(filename: str, books: list, label_layout: BaseLabel) -> bool:
    """
    Polymorphic processing engine. Ingests a collection of Book objects 
    and drives them onto sequential single-sheet canvas pages.
    """
    if not books:
        loging.warning(f"Process aborted for '{filename}': Input book list is empty.")
        return False

    # Extract our stateful physical dimensions right from the active label object
    page_width = label_layout.width
    page_height = label_layout.height
    
    logging.info(f"Opening continuous canvas stream: {page_width/mm:.1f}mm x {page_height/mm:.1f}mm")
    
    try:
        # Instantiate the ReportLab canvas using the dimensions the label instance owns
        c = canvas.Canvas(filename, pagesize=(page_width, page_height))
        
        for index, book in enumerate(books):
            # Safe type-guarding check for students
            if not isinstance(book, Book):
                logging.error(f"Record index {index} is not a valid Book instance object. Skipping.")
                continue
                
            # Polymorphic execution: the orchestrator doesn't care what layout it is drawing!
            label_layout.draw(c, book)
            
            # Roll forward: Tells ReportLab this label is done, append a new page
            c.showPage()
            
        # Commit the binary PDF payload to the Linux filesystem
        c.save()
        logging.info(f"Successfully compiled continuous file stream: '{filename}' ({len(books)} pages written).")
        return True
        
    except Exception as e:
        logging.critical(f"Spooler engine compilation error: {e}")
        return False
