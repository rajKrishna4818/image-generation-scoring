import streamlit as st
import requests

# API Endpoint
API_ENDPOINT = "http://127.0.0.1:8000/generate_ad/"

st.title("Ad Creative Generator & Scorer")

# User inputs
st.write("## Basic Details")
product_name = st.text_input("Product Name", "GlowWell Skin Serum")
tagline = st.text_input("Tagline", "Radiance Redefined.")
colors = st.text_area("Brand Palette (Comma-separated Hex Codes)")  # Allow hex codes
cta_text = st.text_input("Call to Action", "Shop Now")

# Optional user inputs
st.write("## Optional Custom Inputs")
user_prompt = st.text_area(
    "Custom Prompt (Optional)", 
    placeholder="Write a custom prompt to influence the image design (e.g., Modern luxury aesthetics)."
)
custom_logo_url = st.text_input("Custom Logo URL (Optional)", "")
custom_product_image_url = st.text_input("Custom Product Image URL (Optional)", "")

# Process colors once - split and clean
colors_list = [c.strip() for c in colors.split(",")]

# Submit button
if st.button("Generate Creative"):
    # Input payload
    input_data = {
        "creative_details": {
            "product_name": product_name,
            "tagline": tagline,
            "brand_palette": colors_list,  # Use the processed hex list
            "dimensions": {"width": 1080, "height": 1080},
            "cta_text": cta_text,
            "logo_url": custom_logo_url if custom_logo_url else "https://example.com/logo.png",
            "product_image_url": custom_product_image_url if custom_product_image_url else "https://example.com/product.png"
        },
        "scoring_criteria": {
            "background_foreground_separation": 20,
            "brand_guideline_adherence": 20,
            "creativity_visual_appeal": 20,
            "product_focus": 20,
            "call_to_action": 20
        }
    }

    # Prepare query parameters for optional prompt
    params = {}
    if user_prompt:
        params["user_prompt"] = user_prompt

    # Make API call
    response = requests.post(API_ENDPOINT, json=input_data, params=params)

    if response.status_code == 200:
        result = response.json()

        # Display the generated creative as a clickable link
        creative_url = result["creative_url"]
        st.markdown(f"**[Click here to view the generated image]({creative_url})**", unsafe_allow_html=True)

        # Display scoring breakdown
        st.write("### Scoring Breakdown")
        st.json(result["scoring"])

        # Display metadata
        st.write("### Metadata")
        st.json(result.get("metadata", {}))
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

