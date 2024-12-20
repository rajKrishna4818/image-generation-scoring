from utils.prompt_generator import create_prompt
from api.stable_diffusion_api import generate_image_from_hf

def main():
    # Get user input
    brand_title = input("Enter brand title: ")
    tagline = input("Enter tagline: ")
    cta = input("Enter Call-to-Action (CTA): ")
    additional_description = input("Enter additional description (optional): ")

    # Generate prompt
    prompt = create_prompt(brand_title, tagline, cta, additional_description)

    # Generate the image
    response = generate_image_from_hf(prompt)

    # Save the image to assets/ directory
    image_path = f"assets/{brand_title.replace(' ', '_').lower()}_ad.png"
    with open(image_path, "wb") as f:
        f.write(response["data"])  # Replace "data" with actual key from API response
    print(f"Advertisement image saved at: {image_path}")

if __name__ == "__main__":
    main()
