#!/usr/bin/env python3

import logging

class Book:

    def __init__(self, title: str, author: str, call_number: str, asset_id: str):
        self.title = str(title).strip()
        self.author = str(author).strip()
        self.call_number = str(call_number).strip().upper()
        self.asset_id = str(asset_id).strip().upper()
        self._validate_fields()
        logging.info(f"Instantiated Book({self.asset_id}, {self.title[:15]}...)")

    def _validate_fields(self):
        if not self.title:
            logging.error("Book title is empty, raising ValueError.")
            raise ValueError("Data Validation Error: Book title cannot be blank.")
        if not self.asset_id:
            logging.error("Asset ID is empty, raising ValueError.")
            raise ValueError("Data Validation Error: Asset ID cannot be blank.")

    def __repr__(self):
        return f"Book({self.asset_id}, {self.title[:15]}...)"


    
