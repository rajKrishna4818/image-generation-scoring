###AI-Powered Advertising Creative Generator and Scorer
A full-stack application for AI-driven ad creative generation and evaluation.
Setup
bashCopy# Clone repository
git clone https://github.com/your-repo/ad-creative-generator.git
cd ad-creative-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app:app --reload

# Run frontend
streamlit run frontend_ui.py
Architecture
Frontend (frontend_ui.py)

Streamlit-based UI
Ad creative generation form
Real-time scoring visualization
History tracking
Asset downloads

Backend
app.py

FastAPI server
Handles creative generation
S3 integration
Scoring pipeline

stable_diffusion_api.py

Hugging Face API integration
Image generation

prompt_generator.py

Structured prompt creation
Brand element placement
Design requirement handling

extract_image_details.py

Text/luminance analysis
Color extraction
Contrast evaluation

score_functions.py
Evaluates:

Text visibility
Brand adherence
Visual appeal
Product focus
CTA effectiveness

color_utils.py

Color conversions/mappings
Distance calculations

s3_uploader.py

AWS S3 management
File uploads
URL generation

Key Features

AI creative generation
Real-time scoring
Brand palette management
Asset downloads
Generation history

Contributing
bashCopy# Fork repository
# Create feature branch
git checkout -b feature-name

# Make changes
# Run tests
# Submit PR
Requirements:

Pass all tests
Add documentation
Include descriptive comments

License
MIT
