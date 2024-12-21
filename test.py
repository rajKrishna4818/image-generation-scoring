from Image_scorer import ImageScorer
brand_palatte = ["#F2B872","#A67244","#BFA38A","#F2E3D5","#73523F"]
test_image = ImageScorer("1.jpg",brand_palatte)

palatte_contrast = test_image.calculate_palatte_contrast()
colour_details_in_image = test_image.extract_palette_details_in_image()
luminance_details = test_image.extract_luminance_details_in_image()
extracted_text = test_image.extract_text_from_image()
print("palatte_contrast ==> ", palatte_contrast , "\n")
print("colour_details_in_image  ==> ", colour_details_in_image, "\n" )
print("luminance_details ==> ", luminance_details , "\n")
print("extracted_text ==> ", extracted_text , "\n")