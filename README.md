
# AI-Powered Advertising Creative Generator and Scorer

A full-stack application for AI-driven ad creative generation and evaluation.

Access the product through this link ->http://15.207.98.140:443/
or


## Setup


### Clone repository
    git clone https://github.com/your-repo/ad-creative-generator.git

    cd ad-creative-generator

### Create virtual environment
    python -m venv venv

    source venv/bin/activate    # Linux/Mac

    venv\Scripts\activate       # Windows

### Install dependencies
    pip install -r requirements.txt

### Run backend
    uvicorn app:app --reload

### Run frontend
    streamlit run frontend_ui.py
## Architecture Overview

The system is designed as a full-stack application, consisting of a **frontend** built with **Streamlit** for the user interface and a **backend** powered by **FastAPI**. The backend handles creative generation, integrates with external APIs, and manages image scoring. Below is a detailed breakdown of the architecture:

### Frontend (`frontend_ui.py`)
- **Streamlit** is used for creating the user interface. It provides an easy-to-use interface that is interactive and responsive for end-users.
- **Features:**
  - A form for users to input details such as product name, tagline, and custom design prompts.
  - Real-time visualization of generated creatives.
  - Display of scoring breakdown with graphical feedback on the performance of the creative.
  - History tracking to view previously generated creatives.
  - Color palette preview that helps users maintain brand consistency.
  - Download functionality for both the generated creative image and detailed scoring report.

### Backend

#### Main Application (`app.py`)
- **FastAPI** is used as the backend framework for handling API requests and responses.
- **Responsibilities:**
  - Coordinates creative generation requests.
  - Integrates with the **Stable Diffusion API** for image generation.
  - Manages interaction with **AWS S3** for storage of generated images and assets.
  - Executes the scoring pipeline, which evaluates the generated creatives against various metrics.

#### Image Generation (`stable_diffusion_api.py`)
- This module interfaces with **Hugging Face's Stable Diffusion API**, which is responsible for generating high-quality images based on structured prompts.
- It takes user inputs such as product name, tagline, and brand guidelines to produce the creative image.
  
#### Prompt Engineering (`prompt_generator.py`)
- Creates and manages structured prompts that are sent to the Stable Diffusion API.
- Ensures proper placement of brand elements (e.g., product image, logo, tagline).
- Incorporates color schemes and design requirements based on user input.

#### Image Analysis (`extract_image_details.py`)
- This module performs post-processing on the generated image:
  - Detects text and evaluates text visibility.
  - Analyzes luminance and brightness to ensure clear visibility.
  - Extracts the color palette and ensures it aligns with brand guidelines.
  - Calculates contrast ratios to ensure design clarity.

#### Scoring System (`score_functions.py`)
- This module implements the scoring logic based on multiple design and branding metrics:
  - **Text Visibility:** Ensures that text is legible and stands out.
  - **Brand Guideline Adherence:** Checks the usage of the brand’s color palette, logo, and typography.
  - **Visual Appeal:** Evaluates the aesthetic qualities of the creative (e.g., composition, layout).
  - **Product Focus:** Measures how prominently the product is featured.
  - **Call-to-Action (CTA) Effectiveness:** Evaluates whether the CTA is visible and compelling.

#### Color Utilities (`color_utils.py`)
- Provides utility functions to handle color operations:
  - Color conversion (e.g., hex to RGB).
  - Predefined color mappings for brand colors.
  - Color distance calculations to measure how closely a color matches the brand palette.

#### Storage (`s3_uploader.py`)
- Manages integration with **AWS S3** for storing generated images and other assets.
- Handles file uploads, image storage, and presigned URL generation for easy access to the files.

### Data Flow
1. **Frontend Interaction:** The user submits inputs such as product name, tagline, and other design preferences via the Streamlit interface.
2. **API Call:** The backend receives the request, generates a structured prompt, and sends it to the Stable Diffusion API for image generation.
3. **Image Generation:** The Stable Diffusion model generates the image based on the prompt provided.
4. **Image Analysis:** Once the image is generated, it is analyzed for adherence to brand guidelines and scoring metrics.
5. **Scoring:** The scoring system evaluates the image against predefined metrics and returns a score.
6. **Return Data:** The results (image, score, and feedback) are sent back to the frontend for user review.
7. **Storage:** The image is stored in AWS S3, and a link is provided to the user for download or further processing.

---

This architecture ensures a streamlined workflow for generating and scoring ad creatives, allowing for real-time feedback and seamless integration between various components.




## API Documentation
The application features a RESTful API built with FastAPI for generating and scoring advertising creatives. Below is a detailed guide to the API endpoints, including input/output contracts, example requests, and responses.

### 1. Base URL
The API is hosted locally during development at:

arduino
Copy code
http://localhost:8000


## 2. Endpoints

### 2.1 Generate Creative
Endpoint: /generate_creative


Method: POST

Description: Generates an advertising creative based on the provided product details and brand guidelines.
Request: Input Contract
The API expects a JSON payload with the following fields:


json
Copy code

{
  "creative_details": {
    "product_name": "GlowWell Skin Serum",
    "tagline": "Radiance Redefined.",
    "brand_palette": ["#FFC107", "#212121", "#FFFFFF"],
    "dimensions": {
      "width": 1080,
      "height": 1080
    },
    "cta_text": "Shop Now",
    "logo_url": "https://example.com/logo.png",
    "product_image_url": "https://example.com/product.png"
  },
  "scoring_criteria": {
    "background_foreground_separation": 20,
    "brand_guideline_adherence": 20,
    "creativity_visual_appeal": 20,
    "product_focus": 20,
    "call_to_action": 20
  }
}
Response: Output Contract

If successful, the API returns a JSON response with the generated creative URL and scoring breakdown:

json
Copy code
{
  "status": "success",
  "creative_url": "https://example.com/generated_creative.png",
  "scoring": {
    "background_foreground_separation": 18,
    "brand_guideline_adherence": 19,
    "creativity_visual_appeal": 16,
    "product_focus": 15,
    "call_to_action": 14,
    "audience_relevance": 9,
    "total_score": 91
  },
  "metadata": {
    "file_size_kb": 320,
    "dimensions": {
      "width": 1080,
      "height": 1080
    }
  }
}

Example cURL Request
bash

Copy code
curl -X POST http://localhost:8000/generate_creative \
-H "Content-Type: application/json" \
-d '{
  "creative_details": {
    "product_name": "GlowWell Skin Serum",
    "tagline": "Radiance Redefined.",
    "brand_palette": ["#FFC107", "#212121", "#FFFFFF"],
    "dimensions": {
      "width": 1080,
      "height": 1080
    },
    "cta_text": "Shop Now",
    "logo_url": "https://example.com/logo.png",
    "product_image_url": "https://example.com/product.png"
  },
  "scoring_criteria": {
    "background_foreground_separation": 20,
    "brand_guideline_adherence": 20,
    "creativity_visual_appeal": 20,
    "product_focus": 20,
    "call_to_action": 20
  }
}'

### 2.2 Analyze Creative
Endpoint: /analyze_creative
Method: POST
Description: Evaluates an uploaded creative for compliance with predefined scoring metrics.
Request: Input Contract
The API expects a JSON payload with the creative URL to analyze:

json
Copy code
{
  "creative_url": "https://example.com/generated_creative.png",
  "scoring_criteria": {
    "background_foreground_separation": 20,
    "brand_guideline_adherence": 20,
    "creativity_visual_appeal": 20,
    "product_focus": 20,
    "call_to_action": 20
  }
}
Response: Output Contract
The response includes the scoring metrics for the analyzed creative:

json
Copy code
{
  "status": "success",
  "scoring": {
    "background_foreground_separation": 18,
    "brand_guideline_adherence": 19,
    "creativity_visual_appeal": 16,
    "product_focus": 15,
    "call_to_action": 14,
    "audience_relevance": 9,
    "total_score": 91
  },
  "metadata": {
    "file_size_kb": 320,
    "dimensions": {
      "width": 1080,
      "height": 1080
    }
  }
}
Example cURL Request
bash
Copy code
curl -X POST http://localhost:8000/analyze_creative \
-H "Content-Type: application/json" \
-d '{
  "creative_url": "https://example.com/generated_creative.png",
  "scoring_criteria": {
    "background_foreground_separation": 20,
    "brand_guideline_adherence": 20,
    "creativity_visual_appeal": 20,
    "product_focus": 20,
    "call_to_action": 20
  }
}'
3. Error Handling
The API provides clear error responses in case of invalid input or processing errors:

Example Error Response
json
Copy code
{
  "status": "error",
  "message": "Invalid input: 'brand_palette' must contain exactly three colors."
}

## Conclusion

The AI-Powered Advertising Creative Generator and Scorer provides a seamless and efficient solution for generating and analyzing ad creatives. By leveraging AI, it ensures adherence to brand guidelines, maximizes visual appeal, and delivers high-quality assets ready for deployment.

We hope this tool helps streamline your creative process and enhances the effectiveness of your advertising campaigns. For further questions, feel free to reach out or contribute to the project!
## Contact

For support or inquiries, please contact:

- **Email:** 21ume043@lnmiit.ac.in 
- **GitHub Issues:** [GitHub Repository](https://github.com/your-repo/ad-creative-generator/issues)  
- **Documentation:** [API Documentation](http://localhost:8000/docs)
## Acknowledgements


We would like to thank the open-source community and tools like FastAPI, Streamlit, and Stable Diffusion, which made this project possible. Special thanks to all contributors who continue to improve this project.
