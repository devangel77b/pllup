#!/usr/bin/env python3

import sys
import unittest
from unittest.mock import MagicMock, patch
from reportlab.lib.units import mm

# Clean explicit package imports from our Step 6 architecture
from book import Book
from labels import SpineLabel,  DEFAULT_FONT


# =====================================================================
# TEST CLASS 1: GEOMETRIC LAYOUT & CANVAS DRAWING MATH
# =====================================================================
class TestLabelLayouts(unittest.TestCase):
    """Verifies that our geometric layout calculations perform smoothly."""

    def setUp(self):
        """
        Isolated setup hook. This ONLY runs before the layout tests below,
        ensuring it never leaks or shadows the data model assertions.
        """
        # 1. Instantiate a perfectly valid Book object for drawing passes
        self.sample_book = Book("Lady Chatterly's Lover", "D.H. Lawrence", "FIC LAW", "B00002")
        
        # 2. Initialize a mock canvas to absorb text commands in memory
        self.mock_canvas = MagicMock()
        
        # 3. Force stringWidth to return exactly 30.0 points for predictable math
        self.mock_canvas.stringWidth.return_value = 30.0

    def test_spine_label_stores_physical_dimensions(self):
        """Verify the instance stores its width and height inside its own self state."""
        spine = SpineLabel(width=50 * mm, height=30 * mm)
        self.assertEqual(spine.width, 50 * mm)
        self.assertEqual(spine.height, 30 * mm)

    def test_spine_label_horizontal_centering_math(self):
        """
        Verify the horizontal alignment equation mathematically.
        Formula: X = (Label Width - String Width) / 2
        Label Width = 50mm (~141.73 points). Mock String Width = 30.0 points.
        Expected Starting X = (141.73 - 30.0) / 2 = 55.86 points.
        """
        spine = SpineLabel(width=50 * mm, height=30 * mm)
        
        # Trigger the drawing loop on our mock canvas
        spine.draw(self.mock_canvas, self.sample_book)
        
        # Calculate our mathematical expectation explicitly
        expected_x = ((50 * mm) - 30.0) / 2
        
        # call_args_list tracks every time drawString was executed: [(x, y, text), ...]
        all_draw_calls = self.mock_canvas.drawString.call_args_list
        
        # Extract the X parameter (index 0 of the positional arguments tuple)
        actual_title_x = all_draw_calls[0][0][0]
        actual_call_x = all_draw_calls[1][0][0]
        
        # Assert both coordinates match our calculated centering geometry precisely
        self.assertAlmostEqual(actual_title_x, expected_x, places=2)
        self.assertAlmostEqual(actual_call_x, expected_x, places=2)


class TestFontRegistrationFallback(unittest.TestCase):
    """Verifies that the try/except block catches errors and defaults to Courier."""

    def setUp(self):
        # CLEANUP SAFETY: If labels.py was imported by other test files earlier, 
        # it is cached in sys.modules. We must wipe that cache to force our 
        # try/except block to run fresh under our test conditions.
        if 'labels' in sys.modules:
            del sys.modules['labels']

    def test_registration_exception_forces_courier_fallback(self):
        """Ensure an environment error in pdfmetrics safely triggers the Courier fallback."""
        
        # 1. We mock 'registerFont' and force it to raise an Exception on purpose.
        # This simulates a broken system where the Ubuntu font files are missing or corrupt.
        with patch('reportlab.pdfbase.pdfmetrics.registerFont') as mock_register:
            mock_register.side_effect = RuntimeError("Font file path not found.")
            
            # 2. NOW we import labels. 
            # This triggers your module's top-level try/except block right now.
            import labels
            
            # 3. Instantiate your SpineLabel under this simulated broken environment
            label = labels.SpineLabel(width=50*mm, height=30*mm)
            
            # 4. ASSERT: Prove that your except block successfully caught the error
            # and gracefully fell back to the built-in Courier font framework.
            self.assertEqual(label.font, "Courier")

    def tearDown(self):
        # Clean up the cache after the test finishes so other test suites aren't affected
        if 'labels' in sys.modules:
            del sys.modules['labels']


        

if __name__ == "__main__":
    unittest.main()
