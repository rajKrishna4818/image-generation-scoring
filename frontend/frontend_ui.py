import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import webbrowser

# Configure page settings
st.set_page_config(
    page_title="Ad Creative Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #FF2B2B;
        }
        .stTextInput>div>div>input {
            background-color: #f0f2f6;
        }
        .success-text {
            color: #28a745;
        }
        .warning-text {
            color: #ffc107;
        }
        .error-text {
            color: #dc3545;
        }
        .stProgress > div > div > div > div {
            background-color: #FF4B4B;
        }
        .image-link {
            color: #FF4B4B;
            text-decoration: underline;
            cursor: pointer;
            padding: 0.5rem 0;
            display: inline-block;
        }
        .image-link:hover {
            color: #FF2B2B;
        }
        .metrics-container {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .custom-info-box {
            background-color: #e8f4f8;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #4B9FFF;
        }
        .color-preview {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            border: 1px solid #ddd;
            border-radius: 3px;
            vertical-align: middle;
        }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_ENDPOINT = "http://backend:80/generate_ad/"

def initialize_session_state():
    """Initialize session state variables"""
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    if 'current_score' not in st.session_state:
        st.session_state.current_score = None
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None

def display_header():
    """Display the application header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎨 Ad Creative Generator & Scorer")
        st.markdown("Generate and analyze high-quality advertising creatives with AI")
    with col2:
        st.markdown("### Current Time")
        st.markdown(datetime.now().strftime("%Y-%m-%d %H:%M"))

def display_sidebar():
    """Display the sidebar with generation history and stats"""
    with st.sidebar:
        st.header("📊 Generation History")
        if st.session_state.generation_history:
            for idx, history in enumerate(st.session_state.generation_history):
                with st.expander(f"Generation #{idx + 1} - {history['product_name']}"):
                    st.write(f"Product: {history['product_name']}")
                    st.write(f"Score: {history['score']:.1f}/100")
                    st.write(f"Time: {history['timestamp']}")
        else:
            st.info("No generation history yet")
        
        if st.session_state.generation_history:
            st.markdown("---")
            st.markdown("### 🎯 Quick Stats")
            avg_score = sum(h['score'] for h in st.session_state.generation_history) / len(st.session_state.generation_history)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Score", f"{avg_score:.1f}")
            with col2:
                st.metric("Total Generations", len(st.session_state.generation_history))

def create_color_preview(colors):
    """Create HTML for color preview"""
    html = '<div style="display: flex; gap: 10px; margin-top: 10px;">'
    for color in colors:
        html += f'<div style="width: 30px; height: 30px; background-color: {color}; border-radius: 5px; border: 1px solid #ccc;"></div>'
    html += '</div>'
    return html

def generate_creative(input_data):
    """Send request to API to generate creative"""
    try:
        response = requests.post(API_ENDPOINT, json=input_data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return None

def display_generator_tab():
    """Display the generator tab content"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Basic Details")
        product_name = st.text_input("Product Name", "GlowWell Skin Serum",
                                 help="Enter your product name")
        
        tagline = st.text_input("Tagline", "Radiance Redefined.",
                             help="Enter your product tagline")
        
        colors = st.text_area("Brand Palette (Comma-separated Hex Codes)",
                           "#FFC107, #212121, #FFFFFF",
                           help="Enter color codes starting with #")
        
        colors_list = [c.strip() for c in colors.split(",")]
        st.markdown(create_color_preview(colors_list), unsafe_allow_html=True)
        
        cta_text = st.text_input("Call to Action", "Shop Now",
                              help="Enter your call-to-action text")

    with col2:
        st.markdown("### 🎨 Optional Customization")
        user_prompt = st.text_area(
            "Custom Prompt",
            placeholder="Add custom design instructions...",
            help="Additional design instructions"
        )
        
        custom_logo_url = st.text_input(
            "Logo URL",
            placeholder="https://example.com/logo.png",
            help="URL to your logo image"
        )
        
        custom_product_image_url = st.text_input(
            "Product Image URL",
            placeholder="https://example.com/product.png",
            help="URL to your product image"
        )

    st.markdown("---")
    
    generate_button = st.button("🚀 Generate Creative", use_container_width=True)
    
    if generate_button:
        with st.spinner("Generating your creative..."):
            input_data = {
                "creative_details": {
                    "product_name": product_name,
                    "tagline": tagline,
                    "brand_palette": colors_list,
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

            if user_prompt:
                input_data["creative_details"]["custom_prompt"] = user_prompt

            result = generate_creative(input_data)
            if result:
                st.session_state.current_result = result
                st.session_state.current_score = result["scoring"]
                st.session_state.generation_history.append({
                    "product_name": product_name,
                    "score": result["scoring"]["total_score"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Creative generated successfully! View it in the Results tab.")

def display_results_tab():
    """Display the results tab content"""
    if st.session_state.current_score and st.session_state.current_result:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🖼️ Generated Creative")
            st.image(st.session_state.current_result["creative_url"], use_container_width=True)
            st.markdown(f'<a href="{st.session_state.current_result["creative_url"]}" target="_blank" class="image-link">🔍 Open Image in New Tab</a>', unsafe_allow_html=True)
            
        with col2:
            st.markdown("### 📊 Scoring Breakdown")
            scores = st.session_state.current_score
            
            for metric, score in scores.items():
                if metric != "total_score":
                    st.markdown(f"**{metric.replace('_', ' ').title()}**")
                    st.progress(score/100)
                    st.markdown(f"{score:.1f}/100")
            
            st.markdown("---")
            st.markdown(f"### Total Score: {scores['total_score']:.1f}/100")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Creative",
                    data=st.session_state.current_result["creative_url"],
                    file_name="creative.png",
                    mime="image/png"
                )
            with col2:
                st.download_button(
                    label="📊 Download Report",
                    data=json.dumps(scores, indent=2),
                    file_name="scoring_report.json",
                    mime="application/json"
                )
    else:
        st.info("Generate a creative to see results here")

def display_help_tab():
    """Display the help tab content"""
    st.markdown("""
    ### 🌟 How to Get the Best Results
    
    #### 1. Product Name & Tagline
    - Use clear, memorable product names
    - Create compelling taglines that highlight unique value
    - Keep text concise but impactful
    
    #### 2. Brand Palette
    - Use hex color codes (#FFFFFF format)
    - Include 2-4 complementary colors
    - Consider color psychology for your brand
    - Test different combinations for best results
    
    #### 3. Custom Prompt Tips
    - Describe specific style preferences
    - Mention key visual elements
    - Include target audience considerations
    - Specify mood or emotional tone
    
    #### 4. Image Requirements
    - Use high-quality logo files
    - Ensure product images are well-lit
    - Recommended size: 1080x1080 pixels
    - Support formats: PNG, JPG
    
    #### 5. Best Practices
    - Test different color combinations
    - Keep text clear and readable
    - Ensure strong contrast ratios
    - Consider mobile viewing experience
    
    #### 6. Scoring System
    Each creative is evaluated on:
    - Background/Foreground Separation
    - Brand Guideline Adherence
    - Creativity & Visual Appeal
    - Product Focus
    - Call to Action Effectiveness
    """)

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    display_sidebar()

    # Main content area
    tabs = st.tabs(["Generator", "Results", "Help"])
    
    with tabs[0]:
        display_generator_tab()

    with tabs[1]:
        display_results_tab()

    with tabs[2]:
        display_help_tab()

if __name__ == "__main__":
    main()