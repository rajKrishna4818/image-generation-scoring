from api.extract_Image_details import extract_details
from PIL import Image, ImageColor
import io

class score:
    def __init__(self, binary_data, brand_palette):
        # Initialize image processor from binary data
        self.image = extract_details(Image.open(io.BytesIO(binary_data["data"])))
        
        # Process brand palette
        self.brand_palette = []
        for color in brand_palette:
            try:
                clean_color = color.strip()
                if not clean_color.startswith('#'):
                    clean_color = '#' + clean_color
                rgb_color = ImageColor.getrgb(clean_color)
                self.brand_palette.append(rgb_color)
            except ValueError as e:
                raise ValueError(f"Invalid color code: {color}. Please use valid hex color codes (e.g., #FF0000)")

    def luminance_score(self):
        output = self.image.extract_luminance_details_in_image()
        exposure = output["exposure_judgment"]
        if(exposure == "Normal Exposure"):
            return output["normal_percentage"]
        elif exposure == "Underexposed":
            return 100 - output["Underexposed_percentage"]
        else:
            return 100 - output["overexposed_percentage"]
    
    def palatte_contrast_score(self):
        output = self.image.calculate_palette_contrast()
        if output >= 21:
            return 100
        elif output == 1:
            return 0
        elif 4 < output < 21:
            # Mapping input range (5 to 20) to output range (50 to 100)
            return int(50 + (output - 5) * (50 / 15))  # Linear mapping
        else:
            # Mapping input range (2 to 3) to output range (0 to 50)
            return int((output - 2) * 50)

    def image_colour_contrast_score(self):
        output = self.image.extract_palette_details_in_image()
        total_percentage = sum(output.values())
        
        if total_percentage == 0:
           return 0

        # Check if any percentage exceeds 60%
        for percentage in output.values():
            if percentage > 60:
                # Map percentage > 60 to range 50 to 0 (100% maps to 0, 60% maps to 50)
                return 50 - ((percentage - 60) * (50 / 40))

        # Calculate variance of percentages to determine equality
        percentages = list(output.values())
        mean_percentage = sum(percentages) / len(percentages)
        variance = sum((p - mean_percentage) ** 2 for p in percentages) / len(percentages)

        # As variance approaches 0 (equal distribution), output approaches 100
        # Normalize variance to range [0, 1] and invert to get closeness to equality
        closeness_to_equality = 1 - min(variance / 100, 1)
        return closeness_to_equality * 100
    
    def text_score(self, input_text):
        default_string = self.image.extract_text_from_image()
        input_words = set(input_text.lower().split())
        default_words = set(default_string.lower().split())

        total_words = len(input_words)
        if total_words == 0:
            return 0

        matched_words = len(input_words & default_words)

        if matched_words == total_words:
            return 100
        elif matched_words == 0:
            return 0
        else:
            return (matched_words / total_words) * 100