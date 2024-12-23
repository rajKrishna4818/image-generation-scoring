# AI-Powered Advertising Creative Generator and Scorer

This is a full-stack application that generates and scores advertising creatives using AI. It features real-time creative generation, scoring based on brand guidelines, and cloud integration for seamless management of assets.

---

## Table of Contents
- [Setup & Installation](#setup--installation)
- [Architecture Overview](#architecture-overview)
- [Key Features](#key-features)
- [Contributing](#contributing)
- [License](#license)

---

## Setup & Installation

### Clone the Repository
```bash
git clone https://github.com/your-repo/ad-creative-generator.git
cd ad-creative-generator
Create a Virtual Environment
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows
Install Dependencies
Install all required Python packages:

bash
Copy code
pip install -r requirements.txt
Run the Backend
Start the FastAPI backend server:

bash
Copy code
uvicorn app:app --reload
Run the Frontend
Launch the Streamlit frontend:

bash
Copy code
streamlit run frontend_ui.py
Architecture Overview
Frontend (frontend_ui.py)
The frontend is built with Streamlit to provide an intuitive and responsive UI for users.

Features:

Ad creative generation form
Real-time scoring visualization
Generation history tracking
Color palette preview
Download capabilities for creatives and reports
Backend
Main Application (app.py)
FastAPI backend server
Handles creative generation requests
Integrates with the Stable Diffusion API
Manages AWS S3 uploads
Coordinates the scoring pipeline
Image Generation (stable_diffusion_api.py)
Interfaces with Hugging Face's Stable Diffusion API
Handles image generation based on structured prompts
Prompt Engineering (prompt_generator.py)
Creates structured prompts for Stable Diffusion
Ensures proper placement of brand elements
Incorporates color schemes and design requirements
Image Analysis (extract_image_details.py)
Analyzes generated images for:

Text detection
Luminance analysis
Color palette extraction
Contrast calculations
Scoring System (score_functions.py)
Evaluates creatives on multiple metrics:

Text visibility
Brand guideline adherence
Visual appeal
Product focus
Call-to-action effectiveness
Color Utilities (color_utils.py)
Color conversion functions
Predefined color mappings
Color distance calculations
Storage (s3_uploader.py)
Manages AWS S3 integration
Handles file uploads and presigned URL generation
Key Features
Dynamic Ad Creative Generation: Automatically generates high-quality ad visuals.
Real-Time Scoring and Feedback: Evaluate creatives instantly with AI-powered scoring.
Brand Color Palette Management: Maintain consistent branding across creatives.
Generation History Tracking: Keep track of previously generated creatives.
Downloadable Assets and Reports: Easily download creatives and detailed scoring reports.
AI-Powered Image Analysis: Analyze key image attributes such as text, luminance, and contrast.
Contributing
We welcome contributions! To contribute:

Fork the repository.
Create a new branch:
bash
Copy code
git checkout -b feature-name
Make your changes.
Run tests to ensure your changes don't break anything.
Submit a pull request (PR).
Before submitting a PR:

Ensure all tests pass.
Include descriptive comments for any new functionality.
Update relevant documentation.

