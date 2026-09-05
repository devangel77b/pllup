#!/usr/bin/env python3

import os
import sys
import logging
from reportlab.lib.units import mm

# Direct dependencies following your exact repo pattern
from importers import TinyCatCSVImporter
from labels import SpineLabel, BarcodeLabel
from clabel_formatter import generate_continuous_label_stream

# Basic logger tracking setup
logging.basicConfig(level=logging.INFO)



def main():
    print("=== Launching Split-Stream TinyCat Print Runner ===")

    #tsv_source_path = 'librarything_devangel77b_202609041716.tsv'
    tsv_source_path = 'marked_catalog.tsv'
    
    if not os.path.exists(tsv_source_path):
        logging.error(f"Provided source file does not exist: {tsv_source_path}")
        sys.exit(1)

    # 2. Ingest books via your custom class
    logging.info(f"Initializing catalog processing for raw source data: {tsv_source_path}")
    importer = TinyCatCSVImporter()
    books = importer.load_catalog(tsv_source_path)
    
    if not books:
        logging.warning("No valid book entries loaded. Extinguishing process.")
        sys.exit(0)

    # 3. Instantiate your verified layouts (matching your physical label media boundaries)
    spine_layout = SpineLabel()
    barcode_layout = BarcodeLabel(marker_text="EVANGELISTA LIBRARY")

    # 4. Fire the single-roll stream spoolers sequentially
    spine_target = "spine_labels.pdf"
    barcode_target = "barcode_labels.pdf"

    print(f"\nProcessing Pipeline 1: Compiling Spine Roll...")
    generate_continuous_label_stream(spine_target, books, spine_layout)

    print(f"Processing Pipeline 2: Compiling Barcode Roll...")
    generate_continuous_label_stream(barcode_target, books, barcode_layout)

    print("\n" + "="*50)
    print("✨ COMPLETE PIPELINE CONVERGENCE ✨")
    print(f" -> Spine Roll Target:   {spine_target}")
    print(f" -> Barcode Roll Target: {barcode_target}")

if __name__ == "__main__":
    main()
