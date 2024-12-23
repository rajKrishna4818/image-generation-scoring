def create_prompt(brand_title, tagline, cta, additional_description=None):
    """
    Create a compelling prompt for Stable Diffusion.

    Args:
        brand_title (str): The name of the brand.
        tagline (str): The tagline for the advertisement.
        cta (str): Call-to-Action text.
        additional_description (str, optional): Any additional details.

    Returns:
        str: A well-crafted prompt for image generation.
    """
    prompt = (
        f"An advertisement for {brand_title} with the tagline '{tagline}'. "
        f"It features a luxurious, premium design with gold and white tones. "
        f"The Call-to-Action is: '{cta}'."
    )
    if additional_description:
        prompt += f" Additional details: {additional_description}."
    return prompt
