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
        Parses the Library of Congress call number into an ordered list of lines.
        Handles missing spaces, multiple cutters, and safeguards volume/copy suffixes.
        """
        clean_call = " ".join(self.call_number.split())
        
        if not clean_call:
            return ["MISSING"]

        # Step 1: Separate class letters from class numbers if squished (e.g., QA76 -> QA 76)
        spaced = re.sub(r'^([A-Z]{1,3})(\d)', r'\1 \2', clean_call)
        
        # Step 2: Separate a number from a cutter if squished (e.g., 76.73.P98 -> 76.73 .P98)
        spaced = re.sub(r'(\d)\s*(\.?[A-Z]\d)', r'\1 \2', spaced)
        
        # Step 3: Separate a cutter string from a trailing publication year (e.g., P982026 -> P98 2026)
        spaced = re.sub(r'([A-Z]\d+)(\d{4})', r'\1 \2', spaced)
        
        # Break into individual working tokens
        tokens = spaced.split()
        if len(tokens) < 2:
            return tokens
            
        # The first two elements are always the core Classification Letters and Numbers
        lines = [tokens[0], tokens[1]]
        
        # Process the remaining trailing elements (cutters, years, suffixes)
        for token in tokens[2:]:
            # If the token matches a cutter structure (optional dot + letter + digit)
            if re.match(r'^\.?[A-Z]\d+', token):
                # Safeguard library volume (V3) and copy (C2) markers from getting a period prefix
                if token.startswith(('V', 'C')) and not token.startswith('.'):
                    # Check if it matches a standard volume/copy layout exclusively (e.g., V1, C2)
                    if re.match(r'^[VC]\d+$', token):
                        lines.append(token)
                        continue
                
                # If it's a true cutter entry, guarantee it has its sorting period prefix
                if not token.startswith('.'):
                    token = '.' + token
                lines.append(token)
            else:
                # Keep regular years or text fallbacks exactly as they arrived
                lines.append(token)

        return lines


                
    def __repr__(self):
        return f"Book({self.asset_id}, {self.title[:15]}...)"


    
