import unittest
from PIL import Image
from PIL import ImageColor
import numpy as np
from ImageScorer import ImageScorer

class TestImageScorer(unittest.TestCase):
    def setUp(self):
        """
        Set up test cases with sample images and palettes.
        """
        # Create a test image dynamically (2x2 pixels)
        self.test_image = Image.fromarray(
            np.array([
                [[255, 193, 7], [33, 33, 33]],  # Gold, Black
                [[255, 255, 255], [255, 193, 7]]  # White, Gold
            ], dtype=np.uint8)
        )
        self.test_image.save("test_image.jpg")
        self.test_image.close()
        # Define a sample brand palette
        self.brand_palette = ["#FFC107", "#212121", "#FFFFFF"]  # Gold, Black, White
        self.scorer = ImageScorer("test_image.jpg",self.brand_palette)

    def test_palette_conversion(self):
        """
        Test if HEX codes are converted correctly to RGB tuples.
        """
        expected_palette = [(255, 193, 7), (33, 33, 33), (255, 255, 255)]
        self.assertEqual(self.scorer.brand_palette, expected_palette)

    def test_calculate_palette_contrast(self):
        """
        Test the contrast calculation for the brand palette.
        """
        # For the given palette, calculate expected contrast manuall

        expected_contrast = (255 + 0.05) / ( 33 + 0.05 )
        calculated_contrast = self.scorer.calculate_palatte_contrast()
        self.assertAlmostEqual(calculated_contrast, expected_contrast, places=2)

    def test_extract_palette_details_in_image(self):
        """
        Test if the function accurately calculates palette details from the image.
        """
        expected_output = {
            (255, 193, 7): 50.0,  # 2/4 pixels are Gold
            (33, 33, 33): 25.0,   # 1/4 pixels are Black
            (255, 255, 255): 25.0 # 1/4 pixels are White
        }
        result = self.scorer.extract_palette_details_in_image()
        self.assertEqual(result, expected_output)

    def tearDown(self):
        """
        Clean up test images after the test runs.
        """
        import os
        os.remove("test_image.jpg")

# Run the tests
if __name__ == "__main__":
    unittest.main()
