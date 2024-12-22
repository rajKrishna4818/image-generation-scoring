import boto3
import os

# AWS S3 Configuration

S3_BUCKET_NAME = "customadgenerator"     # Replace with your S3 bucket name
AWS_ACCESS_KEY= 'AKIAXNGUU7TZRV7GFHXF'
AWS_SECRET_KEY= 'uSmB5V33KeR+YirEi/cxYZGe9zHsee/UBhUoSPKR'
S3_REGION='ap-south-1'
def upload_to_s3(file_path, object_name):
    """
    Upload a file to an S3 bucket.

    Args:
        file_path (str): Path to the file to upload.
        object_name (str): The name of the file in the S3 bucket.

    Returns:
        str: The public URL of the uploaded file.
    """
    try:
        # Create an S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=S3_REGION
        )

        # Upload the file
        s3_client.upload_file(file_path, S3_BUCKET_NAME, object_name)

        # Generate the public URL
        s3_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{object_name}"
        return s3_url
    except Exception as e:
        raise ValueError(f"Error uploading to S3: {str(e)}")
