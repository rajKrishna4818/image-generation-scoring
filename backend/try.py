import os
import requests
from gradio_client import Client

def test_hf_connection(space_id, hf_token=None):
    """
    Test the connection to the Hugging Face Space.

    Args:
        space_id (str): The ID of the Hugging Face Space.
        hf_token (str, optional): Hugging Face authentication token (if required).

    Returns:
        str: Success or failure message.
    """
    try:
        # Create the Gradio Client
        client = Client(space_id, hf_token=hf_token)
        print(f"Successfully connected to Hugging Face Space: {space_id}")
        return client
    except Exception as e:
        return f"Connection failed: {e}"


def test_hf_predict(client, prompt):
    """
    Test the predict functionality of the Hugging Face Space.

    Args:
        client (Client): The Gradio client instance.
        prompt (str): A text prompt for image generation.

    Returns:
        str: Success message or error details.
    """
    try:
        print(f"Sending prompt: {prompt}")
        result = client.predict(param_0=prompt, api_name="/predict")
        print("Result from Hugging Face API:", result)

        # Check if the result is a file path
        if os.path.exists(result):
            print(f"Image generated and saved locally at: {result}")
            return f"Local file path: {result}"

        # Check if the result is a URL
        if result.startswith("http"):
            print(f"Image available at URL: {result}")
            return f"URL: {result}"

        # Unexpected result
        return f"Unexpected response from Hugging Face API: {result}"

    except Exception as e:
        return f"Prediction failed: {e}"


def main():
    # Configuration
    space_id = "Saarthak2002/stabilityai-stable-diffusion-xl-base-1.0"
    hf_token = "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"  # Replace with your token
    prompt = "A futuristic cityscape at sunset, 4k resolution"

    # Step 1: Test Connection
    print("Testing Hugging Face connection...")
    client = test_hf_connection(space_id, hf_token)
    if isinstance(client, str):
        print(client)  # Print the error message
        return

    # Step 2: Test Prediction
    print("\nTesting image generation...")
    result = test_hf_predict(client, prompt)
    print(result)


if __name__ == "__main__":
    main()
