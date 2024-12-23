def create_prompt(brand_title, tagline, cta, brand_palette, additional_description=None, user_design_style=None, logo_url=None, product_image_url=None):
    """
    Create a structured prompt for Stable Diffusion that ensures clear visibility of all elements.

    Args:
        brand_title (str): The name of the brand
        tagline (str): The tagline for the advertisement
        cta (str): Call-to-Action text
        brand_palette (list): List of brand colors in name format
        additional_description (str, optional): Additional details
        user_design_style (str, optional): Specific design style
        logo_url (str, optional): URL of the brand logo
        product_image_url (str, optional): URL of the product image

    Returns:
        str: A detailed prompt for image generation
    """
    # Start with layout structure
    prompt = (
        f"Create a professional advertisement with clear visual hierarchy. "
        f"The layout should have these distinct sections from top to bottom:\n"
        f"1. Large, clear brand name '{brand_title}' at the top in {brand_palette[0] if brand_palette else 'black'} color\n"
        f"2. Prominent tagline '{tagline}' below the brand name\n"
    )

    # Add product/logo placement instructions
    if product_image_url or logo_url:
        prompt += "3. Central area containing "
        if product_image_url and logo_url:
            prompt += f"both the product image and company logo, balanced composition\n"
        elif product_image_url:
            prompt += f"a prominent product image as the focal point\n"
        else:
            prompt += f"the company logo as a key visual element\n"
    else:
        prompt += (
            "3. Central area with a striking visual representation related to the brand, "
            "using professional advertising photography style\n"
        )

    # Add CTA button instructions
    prompt += (
        f"4. At the bottom, a large, clearly visible button with '{cta}' text "
        f"in {brand_palette[0] if brand_palette else 'white'} text on a "
        f"{brand_palette[1] if len(brand_palette) > 1 else 'contrasting'} background\n"
    )

    # Color scheme instructions
    if brand_palette:
        colors = ", ".join(brand_palette)
        prompt += (
            f"\nColor scheme: Use {colors} as the main colors. "
            f"Primary elements in {brand_palette[0]}, "
            f"secondary elements in {', '.join(brand_palette[1:] if len(brand_palette) > 1 else [brand_palette[0]])}"
        )

    # Design style and quality requirements
    prompt += (
        "\nStyle requirements:"
        "\n- High contrast between elements for maximum readability"
        "\n- Clean, modern design with professional advertising aesthetics"
        "\n- Text must be large and clearly readable"
        "\n- Proper spacing between elements"
        f"{f'- {user_design_style}' if user_design_style else ''}"
    )

    # Additional description if provided
    if additional_description:
        prompt += f"\n\nAdditional details: {additional_description}"

    return prompt