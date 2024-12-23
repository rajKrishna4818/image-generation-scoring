from PIL import Image
import numpy as np
import cv2
from collections import Counter

class extract_details:
    def __init__(self, image):
        """
        Initialize with a PIL Image object.
        Converts to various formats needed for different analyses.
        """
        self.pil_image = image
        # Convert PIL image to numpy array for OpenCV operations
        self.cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        # Create grayscale version for luminance analysis
        self.gray_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
        
    def extract_luminance_details_in_image(self):
        """
        Analyze image exposure by looking at luminance distribution.
        Returns details about normal, under-, and over-exposed regions.
        """
        # Calculate histogram
        hist = cv2.calcHist([self.gray_image], [0], None, [256], [0, 256])
        
        # Define exposure ranges and convert to Python float
        underexposed = float(np.sum(hist[0:85]) / np.sum(hist) * 100)
        normal = float(np.sum(hist[85:170]) / np.sum(hist) * 100)
        overexposed = float(np.sum(hist[170:]) / np.sum(hist) * 100)
        
        # Determine overall exposure judgment
        exposure_type = "Normal Exposure"
        if underexposed > max(normal, overexposed):
            exposure_type = "Underexposed"
        elif overexposed > max(normal, underexposed):
            exposure_type = "Overexposed"
            
        return {
            "exposure_judgment": exposure_type,
            "normal_percentage": normal,
            "Underexposed_percentage": underexposed,
            "overexposed_percentage": overexposed
        }

    def calculate_palette_contrast(self):
        """
        Calculate contrast ratios between dominant colors in the image.
        Returns the average contrast ratio as a Python float.
        """
        # Extract dominant colors
        colors = self._get_dominant_colors(5)  # Get top 5 colors
        
        # Calculate contrast ratios between all color pairs
        contrast_ratios = []
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                contrast = self._calculate_contrast_ratio(colors[i], colors[j])
                contrast_ratios.append(float(contrast))
        
        # Return average contrast ratio
        return float(np.mean(contrast_ratios) if contrast_ratios else 1.0)

    def extract_palette_details_in_image(self):
        """
        Extract color distribution details from the image.
        Returns percentage of each dominant color.
        """
        # Resize image for faster processing while maintaining color distribution
        small_image = cv2.resize(self.cv_image, (150, 150))
        pixels = small_image.reshape(-1, 3)
        
        # Quantize colors to reduce noise
        pixels = np.floor_divide(pixels, 32) * 32
        
        # Count color occurrences
        color_counts = Counter(map(tuple, pixels))
        total_pixels = sum(color_counts.values())
        
        # Calculate percentages for top colors and convert to Python dict with string keys
        color_percentages = {}
        for color, count in sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            percentage = float((count / total_pixels) * 100)
            color_key = f"rgb_{color[0]}_{color[1]}_{color[2]}"
            color_percentages[color_key] = percentage
            
        return color_percentages

    def extract_text_from_image(self):
        """
        Fallback text extraction when OCR is not available.
        Returns empty string to maintain functionality without Tesseract.
        """
        return ""

    def _get_dominant_colors(self, n_colors=5):
        """
        Helper method to extract dominant colors using k-means clustering.
        Returns colors as Python lists instead of numpy arrays.
        """
        pixels = np.float32(self.cv_image).reshape(-1, 3)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        return [color.tolist() for color in palette]

    def _calculate_contrast_ratio(self, color1, color2):
        """
        Helper method to calculate contrast ratio between two colors.
        Returns Python float instead of numpy float32.
        """
        def relative_luminance(rgb):
            rgb = np.array(rgb) / 255.0
            rgb = np.where(rgb <= 0.03928, rgb/12.92, ((rgb + 0.055)/1.055) ** 2.4)
            return float(np.dot(rgb, [0.2126, 0.7152, 0.0722]))

        l1 = relative_luminance(color1)
        l2 = relative_luminance(color2)
        
        max_l = max(l1, l2)
        min_l = min(l1, l2)
        
        return float((max_l + 0.05) / (min_l + 0.05))