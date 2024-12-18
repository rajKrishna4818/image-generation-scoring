## brand_palette need to be an array
from PIL import ImageColor

class ImageScorer :
     def __init__(self, image_path, brand_palette):
        self.image_path = image_path
        self.brand_palette = []
        for i in brand_palette:
             self.brand_palette.append(ImageColor.getrgb(i)) ##convereting hec code to rgb
        self.image = self._load_image()

     def _load_image(self):
            from PIL import Image
            return Image.open(self.image_path)
     
     def calculate_contrast(self):
        def luminance(color):
            return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
        max_luminance = 0
        min_luminance = 500
        for i in self.brand_palette:
             temp = luminance(i)
             max_luminance = max(temp,max_luminance)
             min_luminance - min(temp,min_luminance)
        