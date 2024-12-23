from fastapi import FastAPI, HTTPException, Query
from api.stable_diffusion_api import generate_image_from_hf
from utils.prompt_generator import create_prompt
import boto3
import os
import uuid
from api.score_functions import score
from pydantic import BaseModel, validator

# Import the color utility functions
from utils.color_utils import find_closest_color

app = FastAPI()

# Models
class CreativeDetails(BaseModel):
    product_name: str
    tagline: str
    brand_palette: list
    dimensions: dict
    cta_text: str
    logo_url: str
    product_image_url: str

    @validator('brand_palette')
    def clean_color_codes(cls, v):
        cleaned_palette = []
        for color in v:
            color = color.strip()
            if not color.startswith('#'):
                color = '#' + color
            cleaned_palette.append(color)
        return cleaned_palette


class RequestPayload(BaseModel):
    creative_details: CreativeDetails
    scoring_criteria: dict

# S3 client setup
s3_client = boto3.client("s3")


# Helper Functions
def upload_to_s3(file_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(
            file_path, bucket_name, s3_key,
            ExtraArgs={"ContentType": "image/png"}
        )
        return s3_key
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {str(e)}")


def generate_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating presigned URL: {str(e)}")


# Function to convert hex color code to color name using color_utils
# Function to convert hex color code to color name using color_utils
def hex_to_name(hex_code):
    try:
        closest_color = find_closest_color(hex_code)
        print(f"Converted {hex_code} to {closest_color}")  # This will print the conversion result
        return closest_color
    except Exception as e:
        print(f"Failed to convert hex code: {hex_code}. Returning hex as is.")  # Simple print instead of logging
        return hex_code


# In app.py, modify the /generate_ad/ endpoint:

@app.post("/generate_ad/") 
def generate_ad(
    payload: RequestPayload,
    user_prompt: str = Query(None, description="Custom prompt provided by the user"),
    user_logo_url: str = Query(None, description="Custom logo URL provided by the user"),
    user_product_image_url: str = Query(None, description="Custom product image URL provided by the user"),
    user_brand_palette: str = Query(None, description="Comma-separated list of user-defined brand colors")
):
    try:
        # Extract creative details
        details = payload.creative_details

        # Process logo and product image URLs
        logo_url = user_logo_url if user_logo_url else details.logo_url
        product_image_url = user_product_image_url if user_product_image_url else details.product_image_url

        # Validate URLs if provided
        if logo_url and not logo_url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid logo URL format")
        if product_image_url and not product_image_url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid product image URL format")

        # Process brand palette
        color_names = []
        if user_brand_palette:
            user_colors = user_brand_palette.split(',')
            for color in user_colors:
                color = color.strip()
                if not color.startswith('#'):
                    color = '#' + color
                color_name = hex_to_name(color)
                color_names.append(color_name)
            details.brand_palette = color_names
        else:
            for color in details.brand_palette:
                color = color.strip()
                if not color.startswith('#'):
                    color = '#' + color
                color_name = hex_to_name(color)
                color_names.append(color_name)
            details.brand_palette = color_names

        # Create the prompt
        prompt = create_prompt(
            brand_title=details.product_name,
            tagline=details.tagline,
            cta=details.cta_text,
            brand_palette=details.brand_palette,
            additional_description=user_prompt if user_prompt else None,
            user_design_style=None,
            logo_url=logo_url if logo_url != "https://example.com/logo.png" else None,
            product_image_url=product_image_url if product_image_url != "https://example.com/product.png" else None
        )

        # Print the final prompt for debugging
        print("Generated prompt:", prompt)


        # Generate image using Stable Diffusion
        image_data = generate_image_from_hf(prompt)

        # Rest of the code remains the same...
        local_file = f"assets/{uuid.uuid4().hex}.png"
        with open(local_file, "wb") as f:
            f.write(image_data["data"])

        if not os.path.exists(local_file):
            raise HTTPException(status_code=500, detail="Generated image file not found locally.")

        bucket_name = "your-s3-bucket-name"
        s3_key = f"generated_images/{uuid.uuid4().hex}.png"
        upload_to_s3(local_file, bucket_name, s3_key)

        presigned_url = generate_presigned_url(bucket_name, s3_key)

        marks = score(image_data, details.brand_palette)
        scoring = {
            "background_foreground_separation": marks.luminance_score(),
            "brand_guideline_adherence": marks.text_score(details.tagline),
            "creativity_visual_appeal": marks.image_colour_contrast_score(),
            "product_focus": marks.luminance_score(),
            "call_to_action": marks.text_score(details.cta_text),
            "audience_relevance": marks.palatte_contrast_score(),
            "total_score": sum([marks.luminance_score(), marks.text_score(details.tagline), 
                marks.image_colour_contrast_score(), marks.luminance_score(), 
                marks.text_score(details.cta_text), marks.palatte_contrast_score()]) / 6
        }

        return {
            "status": "success",
            "creative_url": presigned_url,
            "scoring": scoring,
            "metadata": {
                "file_size_kb": os.path.getsize(local_file) / 1024,
                "dimensions": details.dimensions,
                "used_colors": details.brand_palette,
                "used_logo": bool(logo_url and logo_url != "https://example.com/logo.png"),
                "used_product_image": bool(product_image_url and product_image_url != "https://example.com/product.png")
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")