#!/usr/bin/env python3

import logging
from book import Book
from labels import SpineLabel
from clabel_formatter import generate_continuous_label_stream

if __name__ == "__main__":
    print("=== Launching Clabel 221B Print Runner ===")
    
    # 1. Instantiate concrete data entities
    catalog_queue = [
        Book(title="The Hobbit", author="J.R.R. Tolkien", call_number="PR6039.032 H63 1973", asset_id="LIB101"),
        Book(title="A Brief History of Time", author="Stephen Hawking", call_number="QB981 .H377 1988", asset_id="LIB102"),
        Book(title="Introduction to Algorithms", author="Thomas H. Cormen", call_number="QA76.6 .C67 1990", asset_id="LIB103")
    ]
    
    # 2. Instantiate our verified, stateful Monospace view layout
    # Defaults natively to our 50mm x 30mm dimensions and registered monospace font
    spine_layout = SpineLabel()
    
    # 3. Fire our targeted single-roll pipeline controller
    output_target = "spine_roll_output.pdf"
    generate_continuous_label_stream(output_target, catalog_queue, spine_layout)
    
    print(f"\nExecution loop complete. Output file written to: {output_target}")
