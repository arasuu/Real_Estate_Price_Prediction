import streamlit as st
import pandas as pd
import pickle

# Load the trained model
with open("RE_Model.pkl", "rb") as file:
    model = pickle.load(file)

# Streamlit app configuration
st.set_page_config(page_title="🏡 Real Estate Price Prediction", layout="centered")

# App title and description
st.title("🏡 Real Estate Price Prediction")
st.write("Enter the property details below to predict the price:")

# Input widgets
col1, col2 = st.columns(2)
with col1:
    year_sold = st.number_input("Year Sold", min_value=1900, max_value=2100, value=2023)
    property_tax = st.number_input("Property Tax ($)", min_value=0, value=600)
    insurance = st.number_input("Insurance Cost ($)", min_value=0, value=200)
    beds = st.number_input("Number of Beds", min_value=0, value=3)
    baths = st.number_input("Number of Baths", min_value=0, value=2)
    
with col2:
    sqft = st.number_input("Square Footage", min_value=0, value=1800, key="soft")
    year_built = st.number_input("Year Built", min_value=1800, max_value=2025, value=1990)
    lot_size = st.number_input("Lot Size (sqft)", min_value=0, value=10000)
    basement = st.checkbox("Basement", value=True)
    popular = st.checkbox("Popular Location", value=True)
    recession = st.checkbox("Sold During Recession")

# Property type toggle
property_type = st.radio("Property Type", ["Bungalow", "Condo"], index=0)

# Calculate derived features
property_age = year_sold - year_built
bungalow = 1 if property_type == "Bungalow" else 0
condo = 1 if property_type == "Condo" else 0

# Create features DataFrame
features = pd.DataFrame({
    "year_sold": [year_sold],
    "property_tax": [property_tax],
    "insurance": [insurance],
    "beds": [beds],
    "baths": [baths],
    "soft": [sqft],  # Using 'soft' as expected by model
    "year_built": [year_built],
    "lot_size": [lot_size],
    "basement": [int(basement)],
    "popular": [int(popular)],
    "recession": [int(recession)],
    "property_age": [property_age],
    "property_type_Bunglow": [bungalow],  # Exact spelling
    "property_type_Condo": [condo]
})

# Debug view (can be commented out in production)
with st.expander("Debug: View Features"):
    st.write("Model expects:", model.feature_names_in_)
    st.write("Features being sent:", features[model.feature_names_in_])

# Prediction button
if st.button("🏠 Predict Price"):
    try:
        # Ensure correct column order
        features = features[model.feature_names_in_]
        prediction = model.predict(features)[0]
        st.success(f"💰 Estimated Price: **${prediction:,.2f}**")
    except Exception as e:
        st.error(f"Prediction failed. Please check your inputs. Error: {str(e)}")
