from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.stable_diffusion_api import generate_image_from_hf
from utils.prompt_generator import create_prompt
import boto3
import os
import uuid

# FastAPI app instance
app = FastAPI()

# Input model for validation
class CreativeDetails(BaseModel):
    product_name: str
    tagline: str
    brand_palette: list
    dimensions: dict
    cta_text: str
    logo_url: str
    product_image_url: str

class RequestPayload(BaseModel):
    creative_details: CreativeDetails
    scoring_criteria: dict

# S3 client setup
s3_client = boto3.client("s3")

def upload_to_s3(file_path, bucket_name, s3_key):
    """
    Upload a file to S3 and return the uploaded file's S3 key.

    Args:
        file_path (str): Local file path to upload.
        bucket_name (str): S3 bucket name.
        s3_key (str): Destination path/key in the S3 bucket.

    Returns:
        str: Uploaded file's S3 key.
    """
    try:
        s3_client.upload_file(
            file_path, bucket_name, s3_key,
            ExtraArgs={"ContentType": "image/png"}
        )
        return s3_key
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {str(e)}")

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL for the object in the S3 bucket.

    Args:
        bucket_name (str): Name of the S3 bucket.
        object_name (str): Path to the object in the bucket.
        expiration (int): Time in seconds for the presigned URL to remain valid.

    Returns:
        str: Presigned URL as a string.
    """
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating presigned URL: {str(e)}")

@app.post("/generate_ad/")
def generate_ad(payload: RequestPayload):
    try:
        # Extract creative details
        details = payload.creative_details
        prompt = create_prompt(
            brand_title=details.product_name,
            tagline=details.tagline,
            cta=details.cta_text,
            additional_description=" ".join(details.brand_palette)
        )
        
        # Generate image using Stable Diffusion
        image_data = generate_image_from_hf(prompt)

        # Save the image locally
        local_file = f"assets/{uuid.uuid4().hex}.png"
        with open(local_file, "wb") as f:
            f.write(image_data["data"])

        # Upload to S3
        bucket_name = "your-s3-bucket-name"
        s3_key = f"generated_images/{uuid.uuid4().hex}.png"
        upload_to_s3(local_file, bucket_name, s3_key)

        # Generate presigned URL
        presigned_url = generate_presigned_url(bucket_name, s3_key)

        # Generate scoring breakdown (mocked for simplicity)
        scoring = {
            "background_foreground_separation": 18,
            "brand_guideline_adherence": 20,
            "creativity_visual_appeal": 19,
            "product_focus": 18,
            "call_to_action": 19,
        }

        return {"creative_url": presigned_url, "scoring": scoring}

    except Exception as e:
        # Log the exception and re-raise it
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
