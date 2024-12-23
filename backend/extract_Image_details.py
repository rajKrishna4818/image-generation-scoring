from PIL import ImageColor
from scipy.spatial import KDTree
from PIL import Image
import numpy as np
import cv2
import pytesseract
import io

class extract_details:
    def __init__(self, binary_data, brand_palette):
        self.brand_palette = []
        for i in brand_palette:
            self.brand_palette.append(ImageColor.getrgb(i))  # Converting hex code to RGB [list of tuples]
        self.image = self._load_image(binary_data)

    def _load_image(self, binary_data):
        """
        Load the image from binary data.

        Args:
            binary_data (bytes): The binary data of the image.

        Returns:
            PIL.Image.Image: The loaded image.
        """
        return Image.open(io.BytesIO(binary_data))

    def calculate_palette_contrast(self):
        def luminance(color):
            return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

        max_luminance = -1
        min_luminance = 500
        for i in self.brand_palette:
            temp = luminance(i)
            max_luminance = max(temp, max_luminance)
            min_luminance = min(temp, min_luminance)

        return (max_luminance + 0.05) / (min_luminance + 0.05)  # Color contrast using palette

    def extract_palette_details_in_image(self):
        """
        Extracts color details from an image based on a predefined palette.

        Returns:
            dict: Percentage contribution of each color in the palette.
        """
        # Convert the image to RGB
        image = self.image.convert("RGB")
        pixels = np.array(image).reshape(-1, 3)  # Flatten the image to a list of pixels

        # Create a KDTree for fast nearest-neighbor lookup
        tree = KDTree(self.brand_palette)

        # Find the nearest palette color for each pixel
        _, indices = tree.query(pixels)

        # Count occurrences of each palette color
        unique, counts = np.unique(indices, return_counts=True)
        total_pixels = len(pixels)

        # Calculate percentage contribution
        color_contribution = {
            tuple(self.brand_palette[i]): round((count / total_pixels) * 100, 2)
            for i, count in zip(unique, counts)
        }

        return color_contribution

    def tearDown(self):
        """
        Clean up test images and close resources after the test runs.
        """
        self.image.close()  # Close the opened image in the scorer

    def extract_luminance_details_in_image(self):
        """
        Analyzes the luminance of an image, generates a luminance histogram,
        and judges exposure levels (underexposed, normal, overexposed).

        Returns:
            dict: Results containing histogram, exposure judgment, and percentages.
        """
        # Convert the image to a NumPy array
        image = np.array(self.image)

        # Convert the image to grayscale to calculate luminance
        image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        luminance = 0.2126 * image_rgb[:, :, 0] + 0.7152 * image_rgb[:, :, 1] + 0.0722 * image_rgb[:, :, 2]

        # Calculate the histogram
        histogram, bin_edges = np.histogram(luminance, bins=256, range=(0, 255))

        # Calculate percentages of underexposed, normal, and overexposed regions
        total_pixels = luminance.size
        underexposed_percentage = np.sum(histogram[:85]) / total_pixels * 100  # Pixels with luminance [0, 85)
        overexposed_percentage = np.sum(histogram[170:]) / total_pixels * 100  # Pixels with luminance [170, 255)
        normal_percentage = 100 - (underexposed_percentage + overexposed_percentage)

        # Determine exposure judgment
        if underexposed_percentage > 50:
            exposure = "Underexposed"
        elif overexposed_percentage > 50:
            exposure = "Overexposed"
        else:
            exposure = "Normal Exposure"

        # Return analysis results
        return {
            "underexposed_percentage": round(underexposed_percentage, 2),
            "normal_percentage": round(normal_percentage, 2),
            "overexposed_percentage": round(overexposed_percentage, 2),
            "exposure_judgment": exposure
        }

    def extract_text_from_image(self):
        """
        Extracts text from an image using Tesseract OCR.

        Returns:
            str: Extracted text from the image.
        """
        # Convert to grayscale
        image = np.array(self.image)

        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Apply thresholding
        _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
        extracted_text = pytesseract.image_to_string(thresh_image)
        return extracted_text
