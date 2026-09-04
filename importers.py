#!/usr/bin/env python3

import csv
import logging
from abc import ABC, abstractmethod
from typing import List
from book import Book

class BaseImporter(ABC):

    @abstractmethod
    def load_catalog(self, source_path: str) -> List[Book]:
        pass

    def clean_text(self, text: str) -> str:
        return str(text).strip() if text is not None else ""

class TinyCatCSVImporter(BaseImporter):

    def load_catalog(self, source_path: str) -> List[Book]:

        with open(source_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter='\t')

            if reader.fieldnames:
                reader.fieldnames = [name.lower().strip() for name in reader.fieldnames]
            else:
                reader.fieldnames = []

            books = []
            for line_no, row in enumerate(reader):
                try:
                    asset_id = (row.get('barcode') or
                                f"TEMP_{line_no:05d}" # defensive fallback
                                )
                    asset_id = self.clean_text(asset_id)
                    author = self.clean_text(row.get('primary author','UNKNOWN AUTHOR'))
                    title = self.clean_text(row.get('title', 'UNKNOWN TITLE'))
                    call_number = self.clean_text(row.get('lc classification','NO LCC'))
                    book = Book(
                        title=title,
                        author=author,
                        call_number=call_number,
                        asset_id=asset_id
                        )
                    books.append(book)

                except Exception as e:
                    logging.error(f"Skipping malformed row on line {line_no}")

        logging.info(f"Successfully processed {len(books)} books via TinyCatCSVImporter")
        return books

        
                    
