import os
import uuid
import requests
from gradio_client import Client
from shutil import copyfile

def generate_image_from_hf(prompt):
    """
    Generate an image using Hugging Face's Stable Diffusion API.

    Args:
        prompt (str): A well-crafted text prompt for image generation.

    Returns:
        dict: Response containing the binary image data.
    """
    try:
        # Instantiate the Hugging Face client
        #client = Client("Saarthak2002/stabilityai-stable-diffusion-xl-base-1.0")
        client = Client("Saarthak2002/stabilityai-stable-diffusion-xl-base-1.0", hf_token="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")
        result = client.predict(param_0=prompt, api_name="/predict")

        print("Result from Hugging Face API:", result)

        # Check if the result is a local file path
        if os.path.exists(result):
            with open(result, "rb") as f:
                image_data = f.read()
            return {"data": image_data}

        # Check if the result is a URL
        if result.startswith("http"):
            response = requests.get(result)
            response.raise_for_status()
            return {"data": response.content}

        # Handle unexpected cases
        raise ValueError(f"Unexpected response from Hugging Face API: {result}")

    except Exception as e:
        raise ValueError(f"Error generating image: {str(e)}")
