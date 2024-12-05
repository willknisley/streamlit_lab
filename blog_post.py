import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('weather_data.csv')

st.title("Warmest Climate Explorer")
st.sidebar.header("Options")

# City Comparison
city = st.sidebar.selectbox("Select a city to view its data", df['city'])
st.subheader(f"Climate Data for {city}")
st.write(df[df['city'] == city].T)

# Composite Score Calculator
st.sidebar.subheader("Adjust Weights")
temp_weight = st.sidebar.slider("Temperature Weight", 0.0, 1.0, 0.5)
feels_like_weight = st.sidebar.slider("Feels-Like Weight", 0.0, 1.0, 0.25)
humidity_weight = st.sidebar.slider("Humidity Weight", 0.0, 1.0, 0.25)

df['custom_score'] = (
    df['temperature'] * temp_weight +
    df['feels_like'] * feels_like_weight +
    df['humidity'] * humidity_weight
)

warmest_city = df.loc[df['custom_score'].idxmax(), 'city']
st.write(f"Warmest city based on your weights: **{warmest_city}**")

# Visualizations
st.subheader("Visualization")
metric = st.selectbox("Select metric to visualize", ['temperature', 'humidity', 'wind_speed'])
fig, ax = plt.subplots()
df.plot(kind='bar', x='city', y=metric, ax=ax)
st.pyplot(fig)

# API Integration (Optional)
st.sidebar.subheader("Add Your Own City")
new_city = st.sidebar.text_input("City Name")
if st.sidebar.button("Fetch Data"):
    st.write(f"Fetching data for {new_city}...")
    # Placeholder for API integration