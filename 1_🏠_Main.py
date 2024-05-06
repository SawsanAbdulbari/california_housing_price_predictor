import streamlit as st
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='California Housing Price Predict',
                   page_icon=":bar_chart:",
                   layout="wide")

st.title(":house_buildings: Welcome to the California Housing Price :red[Predictor!] ")

image = "img.png"
st.sidebar.image(image, caption='California Housing AI', use_column_width=True)

st.sidebar.write("Final project for Python Machine Learning Diploma📊📈")
st.sidebar.write("")

# Signature
st.sidebar.write("")
st.sidebar.markdown(
    "Made with :green_heart: by "
    "[Linda Marin](https://www.linkedin.com/in/lindamarin97/) & [Sawsan Abdulbari](https://www.linkedin.com/in/sawsanabdulbari/)")

st.markdown("""
This interactive app allows you to explore and 
predict housing prices across California districts based on various features.
Navigate through the app to explore data, gain insights, and make your own predictions.
""")

st.header('How to Use This App')
st.markdown("""
- Navigate using the sidebar to access different features of the app.
- **Explore Data:** View and interact with housing data visualizations.
- **Make Predictions:** Input housing features to predict prices in different districts.
""")
# We added error handling for file operations.
try:
    df = pd.read_csv('housing.csv')
except FileNotFoundError:
    st.error("Error: 'housing.csv' file not found.")
    st.stop()
st.header('Features')
st.markdown("""
- **Data Exploration:** Dive deep into the housing dataset with interactive charts and maps.
- **Price Prediction:** Use our machine learning model to estimate house prices.
- **Download Data:** Access and download the dataset for your own analysis.
""")

# Load and display data (with error handling)
try:
    df = pd.read_csv('housing.csv')
except FileNotFoundError:
    st.error("Error: 'housing.csv' file not found.")
    st.stop()

# Quick data exploration feature
st.header('Quick Explore')
if st.button('Show Median Prices Map'):
    data = df[['latitude', 'longitude']]
    st.map(data)

st.header('About')
st.markdown("""
This app was created with :green_heart: 
by :green[Linda Marin & Sawsan Abdulbari] as Final project for Python Machine 
Learning Diploma📊📈 to explore housing data and predictive modeling.
For more information, contributions, or questions, 
please visit our <a href="https://www.linkedin.com/in/lindamarin97/" target="_blank">LinkedIn</a> profile.
""", unsafe_allow_html=True)


# Add a footer
footer="""
<style>
.footer a:link, .footer a:visited{
    color: red;
    background-color: transparent;
    text-decoration: underline;
}

.footer a:hover, .footer a:active {
    color: blue;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="footer">
<p>Developed with <span style='color:red;'>❤</span> by <a href="https://www.linkedin.com/in/lindamarin97/" target="_blank">Linda Marin </a> &
<a href="https://www.linkedin.com/in/sawsanabdulbari/" target="_blank">Sawsan Abdulbari</a></p>

</div>
"""
st.markdown(footer,unsafe_allow_html=True)
