import streamlit as st
import requests

API_ENDPOINT = "http://127.0.0.1:8000/generate_ad/"

st.title("Ad Creative Generator & Scorer")

# User inputs
product_name = st.text_input("Product Name", "GlowWell Skin Serum")
tagline = st.text_input("Tagline", "Radiance Redefined.")
colors = st.text_area("Brand Palette (Comma-separated)", "#FFC107, #212121, #FFFFFF")
cta_text = st.text_input("Call to Action", "Shop Now")
logo_url = st.text_input("Logo URL", "https://example.com/logo.png")
product_image_url = st.text_input("Product Image URL", "https://example.com/product.png")

# Submit button
if st.button("Generate Creative"):
    # Input payload
    input_data = {
        "creative_details": {
            "product_name": product_name,
            "tagline": tagline,
            "brand_palette": colors.split(","),
            "dimensions": {"width": 1080, "height": 1080},
            "cta_text": cta_text,
            "logo_url": logo_url,
            "product_image_url": product_image_url
        },
        "scoring_criteria": {
            "background_foreground_separation": 20,
            "brand_guideline_adherence": 20,
            "creativity_visual_appeal": 20,
            "product_focus": 20,
            "call_to_action": 20
        }
    }

    # Make API call
    response = requests.post(API_ENDPOINT, json=input_data)

    if response.status_code == 200:
        result = response.json()

        # Display the generated creative as a clickable link
        creative_url = result["creative_url"]
        st.markdown(f"**[Click here to view the generated image]({creative_url})**", unsafe_allow_html=True)

        # Display scoring breakdown
        st.write("### Scoring Breakdown")
        st.json(result["scoring"])
    else:
        st.error(f"Error: {response.status_code}")
