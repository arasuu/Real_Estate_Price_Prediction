import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the trained model
with open("RE_Model.pkl", "rb") as file:
    model = pickle.load(file)

# Set page configuration with a real estate theme
st.set_page_config(page_title="🏡 Real Estate Price Prediction", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("🏡 Real Estate Price Prediction")
st.write("Enter the property details below to predict the price:")

# Collect user inputs
year_sold = st.number_input("Year Sold", min_value=1900, max_value=2100, value=2011)
property_tax = st.number_input("Property Tax ($)", min_value=0, value=520)
insurance = st.number_input("Insurance Cost ($)", min_value=0, value=158)
beds = st.number_input("Number of Beds", min_value=0, value=4)
baths = st.number_input("Number of Baths", min_value=0, value=2)
sqft = st.number_input("Square Footage", min_value=0, value=2300)
year_built = st.number_input("Year Built", min_value=1800, max_value=2025, value=1970)
lot_size = st.number_input("Lot Size (sqft)", min_value=0, value=15245)

# ✅ Yes/No Toggles for Binary Inputs
basement = st.toggle("Does it have a Basement?")
popular = st.toggle("Is it in a Popular Location?")
recession = st.toggle("Was it sold during a Recession?")

# Convert toggles to binary values
basement = 1 if basement else 0
popular = 1 if popular else 0
recession = 1 if recession else 0

property_type = st.radio("Property Type", ["Bungalow", "Condo"], index=0)

# Convert radio button selection to binary values
bungalow = 1 if property_type == "Bungalow" else 0
condo = 1 if property_type == "Condo" else 0

# Reorder columns if model expects a specific order
if hasattr(model, "feature_names_in_"):
    features = features[model.feature_names_in_]

# Replace your features array with this:
features = pd.DataFrame({
    "year_sold": [year_sold],
    "property_tax": [property_tax],
    "insurance": [insurance],
    "beds": [beds],
    "baths": [baths],
    "sqft": [sqft],
    "year_built": [year_built],
    "lot_size": [lot_size],
    "basement": [basement],
    "popular": [popular],
    "recession": [recession],
    "age_when_sold": [year_sold - year_built],  # Adjust column name if needed
    "bungalow": [bungalow],
    "condo": [condo]
})



# Predict button
if st.button("🏠 Predict Price"):
    prediction = model.predict(features)[0]
    st.success(f"💰 Estimated Price: **${prediction:,.2f}**")

