## brand_palette need to be an array
from PIL import ImageColor
from scipy.spatial import KDTree
from PIL import Image
import numpy as np

class ImageScorer :
    def __init__(self, image_path, brand_palette):
        self.image_path = image_path
        self.brand_palette = []
        for i in brand_palette:
             self.brand_palette.append(ImageColor.getrgb(i)) ##convereting hec code to rgb [list of touple]
        self.image = self._load_image()

    def _load_image(self):
            from PIL import Image
            return Image.open(self.image_path)
    
    def close_image(self):
        """Close the image file."""
        if self.image:
            self.image.close()
     
    def calculate_palatte_contrast(self):
        def luminance(color):
            return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
        max_luminance = -1
        min_luminance = 500
        for i in self.brand_palette:
             temp = luminance(i)
             max_luminance = max(temp,max_luminance)
             min_luminance = min(temp,min_luminance)

        return (max_luminance + 0.05) / (min_luminance + 0.05) ## colour contrast by using palette

    def extract_palette_details_in_image(self):
        """
        Extracts color details from an image based on a predefined palette.
        
        Args:
            image_path (str): Path to the input image.
            palette (list): List of RGB colors in the palette.
            
        Returns:
            dict: Percentage contribution of each color in the palette.
        """
        # Load the image and convert to RGB
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
        self.image.close()  # Close the opened image in the score