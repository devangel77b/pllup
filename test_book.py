#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock
from reportlab.lib.units import mm

from book import Book

class TestBook(unittest.TestCase):

    def test_valid_book_instantiation(self):
        book = Book("The Hobbit","J.R.R. Tolkien", "FIC TOL", "B00001")
        self.assertEqual(book.title, "The Hobbit")
        self.assertEqual(book.call_number,"FIC TOL")
        self.assertEqual(book.asset_id,"B00001")

    def test_missing_title_raises_value_error(self):
        with self.assertRaises(ValueError):
            Book(title="",author="D H Lawrence",call_number="FIC LAW",asset_id="B00002")

    def test_missing_asset_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            Book(title="Lady Chatterley's Lover",author="D H Lawrence",call_number="FIC LAW",asset_id="")


class TestBookCallNumberParsing(unittest.TestCase):

    def setUp(self):
        """Set up standard default values for mandatory text validations."""
        self.default_title = "Test Title"
        self.default_author = "Test Author"
        self.default_asset = "A101"

    def test_standard_spaced_call_number(self):
        """Verify parsing of clean, perfectly spaced Library of Congress strings."""
        book = Book(self.default_title, self.default_author, "QA 76.73 .P98 2026", self.default_asset)
        expected = ["QA", "76.73", ".P98", "2026"]
        self.assertEqual(book.call_number_lines, expected)

    def test_squished_no_spaces(self):
        """Verify regex can break down characters with absolutely zero whitespace padding."""
        book = Book(self.default_title, self.default_author, "QA76.73.P982026", self.default_asset)
        expected = ["QA", "76.73", ".P98", "2026"]
        self.assertEqual(book.call_number_lines, expected)

    def test_missing_cutter_dot_restoration(self):
        """Ensure an explicit sorting period is automatically added if a cutter is unspaced."""
        book = Book(self.default_title, self.default_author, "QA76.73 P98 2026", self.default_asset)
        expected = ["QA", "76.73", ".P98", "2026"]
        self.assertEqual(book.call_number_lines, expected)

    def test_multiple_cutters_and_extra_elements(self):
        """Verify handling of complex shelf entries containing secondary cutters or copy identifiers."""
        book = Book(self.default_title, self.default_author, "QA 273 .A1 .B23 2026 V3 C2", self.default_asset)
        expected = ["QA", "273", ".A1", ".B23", "2026", "V3", "C2"]
        self.assertEqual(book.call_number_lines, expected)

    def test_case_insensitivity_and_whitespace_clipping(self):
        """Check that lower case input strings normalize perfectly to standard capitalized tokens."""
        book = Book(self.default_title, self.default_author, "  qa  76.73  .p98  ", self.default_asset)
        expected = ["QA", "76.73", ".P98"]
        self.assertEqual(book.call_number_lines, expected)

    def test_non_standard_fallback(self):
        """Ensure unconventional call sequences degrade safely into standard whitespace blocks."""
        book = Book(self.default_title, self.default_author, "FICTION KING 1999", self.default_asset)
        expected = ["FICTION", "KING", "1999"]
        self.assertEqual(book.call_number_lines, expected)

    def test_missing_or_blank_call_number(self):
        """Confirm that a completely empty string falls back cleanly to a sentinel line."""
        book = Book(self.default_title, self.default_author, "   ", self.default_asset)
        self.assertEqual(book.call_number_lines, ["MISSING"])

            
            
if __name__ == "__main__":
    unittest.main()
