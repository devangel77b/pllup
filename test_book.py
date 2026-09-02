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

if __name__ == "__main__":
    unittest.main()
