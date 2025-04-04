import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open('RE_Model.pkl', 'rb') as file:
    model = pickle.load(file)

# Streamlit UI
st.title("🏡 Real Estate Price Prediction App")
st.write("Enter the property details below to predict the price:")

# Collect user inputs
year_sold = st.number_input("Year Sold", min_value=1900, max_value=2100, value=2011)
property_tax = st.number_input("Property Tax", min_value=0, value=520)
insurance = st.number_input("Insurance Cost", min_value=0, value=158)
beds = st.number_input("Number of Beds", min_value=0, value=4)
baths = st.number_input("Number of Baths", min_value=0, value=2)
sqft = st.number_input("Square Footage", min_value=0, value=2300)
year_built = st.number_input("Year Built", min_value=1800, max_value=2100, value=1970)
lot_size = st.number_input("Lot Size (sq ft)", min_value=0, value=15245)
basement = st.radio("Basement", [0, 1])
popular = st.radio("Popular Location", [0, 1])
recession = st.radio("During Recession?", [0, 1])
property_age = year_sold - year_built  # Auto-calculate
property_type = st.selectbox("Property Type", ["Bungalow", "Condo"])

# Encode property type
property_type_Bungalow = 1 if property_type == "Bungalow" else 0
property_type_Condo = 1 if property_type == "Condo" else 0

# Create feature array
features = np.array([[year_sold, property_tax, insurance, beds, baths, sqft, year_built, 
                      lot_size, basement, popular, recession, property_age, 
                      property_type_Bungalow, property_type_Condo]])

# Predict button
if st.button("Predict Price"):
    price = model.predict(features)[0]
    st.success(f"🏡 Estimated Price: **${price:,.2f}**")

