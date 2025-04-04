import streamlit as st
import pandas as pd
import pickle
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# --- Load Model ---
@st.cache_resource
def load_model():
    with open("RE_Model.pkl", "rb") as file:
        return pickle.load(file)
model = load_model()

# --- Page Config ---
st.set_page_config(
    page_title="🏡 AI Property Valuator",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
    }
    
    .property-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .property-card:hover {
        transform: translateY(-5px);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(107, 115, 255, 0.4);
    }
    
    .price-display {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
colored_header(
    label="🏡 AI Property Valuator",
    description="Instant home valuation powered by machine learning",
    color_name="blue-70"
)

# --- Input Section ---
with st.container():
    st.subheader("📋 Property Details")
    
    with stylable_container(
        key="property_card",
        css_styles="""
            {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
        """
    ):
        col1, col2 = st.columns(2)
        
        with col1:
            year_sold = st.slider("Year Sold", 2000, 2025, 2023)
            property_tax = st.number_input("Annual Property Tax ($)", min_value=0, value=6000, step=500)
            insurance = st.number_input("Annual Insurance ($)", min_value=0, value=2000, step=100)
            sqft = st.slider("Square Footage", 500, 10000, 2500, 100, key="soft")
            
        with col2:
            beds = st.selectbox("Bedrooms", [1, 2, 3, 4, 5, 6], index=2)
            baths = st.select_slider("Bathrooms", [1, 1.5, 2, 2.5, 3, 3.5, 4])
            year_built = st.slider("Year Built", 1900, 2025, 1990)
            lot_size = st.number_input("Lot Size (sqft)", min_value=0, value=10000, step=500)
        
        st.markdown("---")
        
        col3, col4, col5 = st.columns(3)
        with col3:
            basement = st.checkbox("Basement", value=True)
        with col4:
            popular = st.checkbox("Prime Location", value=True)
        with col5:
            recession = st.checkbox("Recession Period", value=False)
        
        property_type = st.radio("Property Type", ["Bungalow", "Condo"], index=0, horizontal=True)

# --- Prediction Logic ---
property_age = year_sold - year_built
bungalow = 1 if property_type == "Bungalow" else 0
condo = 1 if property_type == "Condo" else 0

features = pd.DataFrame({
    "year_sold": [year_sold],
    "property_tax": [property_tax],
    "insurance": [insurance],
    "beds": [beds],
    "baths": [baths],
    "sqft": [sqft],
    "year_built": [year_built],
    "lot_size": [lot_size],
    "basement": [int(basement)],
    "popular": [int(popular)],
    "recession": [int(recession)],
    "property_age": [property_age],
    "property_type_Bunglow": [bungalow],
    "property_type_Condo": [condo],
})

# --- Prediction Button ---
if st.button("✨ Estimate Property Value", use_container_width=True):
    try:
        features = features[model.feature_names_in_]
        prediction = model.predict(features)[0]
        
        with stylable_container(
            key="result_container",
            css_styles="""
                {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    margin-top: 30px;
                    text-align: center;
                }
            """
        ):
            st.balloons()
            st.success("Valuation Complete!")
            st.markdown(f'<div class="price-display">${prediction:,.2f}</div>', unsafe_allow_html=True)
            
            # Market comparison
            col6, col7, col8 = st.columns(3)
            with col6:
                st.metric("Price/SqFt", f"${prediction/sqft:,.2f}")
                       
    except Exception as e:
        st.error(f"Valuation failed: {str(e)}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>© 2025 AI Property Valuator | <a href="#" style="color: #666;">Terms</a> | <a href="#" style="color: #666;">Privacy</a></p>
    <p>This estimate is provided for informational purposes only</p>
</div>
""", unsafe_allow_html=True)
