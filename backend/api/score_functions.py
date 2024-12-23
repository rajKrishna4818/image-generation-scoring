from api.extract_Image_details import extract_details
from PIL import Image, ImageColor
import io
from utils.color_utils import color_names  # Import the color dictionary

class score:
    def __init__(self, binary_data, brand_palette):
        # Initialize image processor from binary data
        self.image = extract_details(Image.open(io.BytesIO(binary_data["data"])))
        
        # Process brand palette - handle both hex codes and color names
        self.brand_palette = []
        for color in brand_palette:
            try:
                clean_color = color.strip().lower()
                if clean_color in color_names:
                    # If it's a color name, get its RGB value
                    rgb_color = color_names[clean_color]
                else:
                    # If it's a hex code, process it normally
                    if not clean_color.startswith('#'):
                        clean_color = '#' + clean_color
                    rgb_color = ImageColor.getrgb(clean_color)
                self.brand_palette.append(rgb_color)
            except (ValueError, KeyError) as e:
                print(f"Warning: Could not process color {color}. Using fallback color.")
                # Use a fallback color (white) instead of raising an error
                self.brand_palette.append((255, 255, 255))
                
    def text_score(self, input_text):
            """
            Calculate text matching score with improved partial matching and word similarity.
            """
            extracted_text = self.image.extract_text_from_image()
            
            # Convert both texts to lowercase and split into words
            input_words = set(input_text.lower().split())
            extracted_words = set(extracted_text.lower().split())
            
            if not input_words:
                return 0
            
            # Count matches using partial matching
            matches = 0
            for input_word in input_words:
                # Check for exact matches
                if input_word in extracted_words:
                    matches += 1
                    continue
                    
                # Check for partial matches (e.g., "button" matches "buttons")
                for extracted_word in extracted_words:
                    if (input_word in extracted_word or 
                        extracted_word in input_word or 
                        self._levenshtein_distance(input_word, extracted_word) <= 2):
                        matches += 0.5  # Partial match counts as half
                        break
            
            # Calculate score
            score = (matches / len(input_words)) * 100
            
            # Print debug information
            print(f"Input text: {input_text}")
            print(f"Extracted text: {extracted_text}")
            print(f"Text score: {score}")
            
            return min(100, score)  # Cap at 100

    def _levenshtein_distance(self, s1, s2):
            """
            Calculate the Levenshtein distance between two strings.
            Used for fuzzy matching of words.
            """
            if len(s1) < len(s2):
                return self._levenshtein_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)
            
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]

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