#!/usr/bin/env python3

import logging
import re

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

    @property
    def call_number_lines(self) -> list:
        """
        Parses the Library of Congress call number into an ordered list of lines 
        suitable for vertical printing on a spine label.
        """
        # Collapse multi-spaces and handle formatting variations safely
        clean_call = " ".join(self.call_number.split())
        
        if not clean_call:
            return ["MISSING"]

        # Regex breakdown:
        # 1. Letters (1-3 alpha) -> e.g., QA
        # 2. Main Number (ints + optional decimals) -> e.g., 76.73
        # 3. First Cutter (optional dot + letter + digits) -> e.g., .P98
        # 4. Trailing data (remaining cutters, volume tags, or publication years)
        pattern = r'^([A-Z]{1,3})\s*(\d+(?:\.\d+)?)(?:\s*(\.?[A-Z]\d+))?(.*)$'
        match = re.match(pattern, clean_call)
        
        if not match:
            # Fallback to a clean whitespace split if the code is highly non-standard
            logging.warning(f"Unconventional LC format for asset {self.asset_id}. Falling back to standard split.")
            return [p for p in clean_call.split(" ") if p]
            
        letters, number, cutter1, remainder = match.groups()
        lines = [letters, number]
        
        if cutter1:
            # Re-verify cutter features a period prefix for strict classification sorting
            if not cutter1.startswith('.'):
                cutter1 = '.' + cutter1
            lines.append(cutter1)
            
        if remainder:
            # Isolate extra tokens (years, copy counts, secondary cutter runs)
            extra_parts = [p.strip() for p in remainder.split(" ") if p.strip()]
            for part in extra_parts:
                # Catch unspaced secondary cutter blocks and restore the period indicator
                if re.match(r'^[A-Z]\d+', part):
                    part = '.' + part
                lines.append(part)
                
        return lines
        
    def __repr__(self):
        return f"Book({self.asset_id}, {self.title[:15]}...)"


    
