import streamlit as st
import pandas as pd
from joblib import load

image = "img.png"
st.sidebar.image(image, caption='Image', use_column_width=True)
st.sidebar.write("Final project for Python Machine Learning Diploma📊📈")
# Signature
st.sidebar.markdown(
    "Made with :green_heart: by "
    "[Linda Marin](https://www.linkedin.com/in/lindamarin97/) & [Sawsan Abdulbari](https://www.linkedin.com/in/sawsanabdulbari/)")

# Page header is set, making the purpose of the page clear to the user
st.title(':house_buildings: :red[California Housing Price Predictor]')
st.write("This application predicts the median house price in California based on input features.")

# Here we load trained model and preprocessing pipeline to be used
model = load('california_model.joblib')
pipeline = load('full_pipeline.joblib')


# We made this function to predict the housing price
# Enhanced error handling is included for detailed messages
def predict_price(input_data):
    try:
        preprocessed_data = pipeline.transform(input_data)
        prediction = model.predict(preprocessed_data)
        return prediction[0], None
    except Exception as e:
        return None, str(e)


# Here we validate the user input
def validate_inputs(input_data):
    errors = []

    # Validating Median Income
    if not (0.0 <= input_data['median_income'][0] <= 15.0):
        errors.append('Median Income must be between 0.0 and 15.0.')

    # Validating Housing Median Age
    if not (1 <= input_data['housing_median_age'][0] <= 52):
        errors.append('Housing Median Age must be between 1 and 52.')

    # Validating Total Rooms
    if input_data['total_rooms'][0] <= 0:
        errors.append('Total Rooms must be greater than 0.')

    # Validating Total Bedrooms
    if input_data['total_bedrooms'][0] < 0:  # 0 is valid if it's a studio
        errors.append('Total Bedrooms cannot be negative.')

    # Validating Population
    if input_data['population'][0] <= 0:
        errors.append('Population must be greater than 0.')

    # Validating Households
    if input_data['households'][0] <= 0:
        errors.append('Households must be greater than 0.')

    # Validating Latitude and Longitude, range was set for area of California, USA
    if not (32.0 <= input_data['latitude'][0] <= 42.0):
        errors.append('Latitude must be between 32.0 and 42.0.')
    if not (-124.3 <= input_data['longitude'][0] <= -114.0):
        errors.append('Longitude must be between -124.3 and -114.0.')

    return errors


# Defining reasonable default values for each input
default_values = {
    'median_income': 3.0,
    'housing_median_age': 30,
    'total_rooms': 1,
    'total_bedrooms': 1,
    'population': 1,
    'households': 1,
    'latitude': 34.0,
    'longitude': -118.0,
    'ocean_proximity': 'NEAR OCEAN',
}


# Initializing the values
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    for key, value in default_values.items():
        # If the key (user input) does not exist in session_state we assign default value to the field
        if key not in st.session_state:
            st.session_state[key] = value


# We created a function to reset inputs to their default values
def reset_inputs():
    """Reset all inputs to their default values."""
    for key, value in default_values.items():
        st.session_state[key] = value


# Adding engineered features with a function
def add_engineered_features(input_df):
    input_df['rooms_per_household'] = input_df['total_rooms'] / input_df['households']
    input_df['bedrooms_per_room'] = input_df['total_bedrooms'] / input_df['total_rooms']
    input_df['population_per_household'] = input_df['population'] / input_df['households']
    return input_df


# Collecting user inputs
def collect_inputs():
    st.session_state['input_data']['median_income'] = median_income
    st.session_state['input_data']['housing_median_age'] = housing_median_age
    st.session_state['input_data']['total_rooms'] = total_rooms
    st.session_state['input_data']['total_bedrooms'] = total_bedrooms
    st.session_state['input_data']['population'] = population
    st.session_state['input_data']['households'] = households
    st.session_state['input_data']['latitude'] = latitude
    st.session_state['input_data']['longitude'] = longitude
    st.session_state['input_data']['ocean_proximity'] = ocean_proximity


# Assigning placeholders for input data
if 'input_data' not in st.session_state:
    st.session_state['input_data'] = {}


# Here we assign a set range for each value
median_income_range = (0.0, 15.0)
housing_median_age_range = (0, 52)
total_rooms_range = (1, 10000)
total_bedrooms_range = (1, 3000)
population_range = (1, 10000)
households_range = (1, 5000)
latitude_range = (32.0, 42.0)
longitude_range = (-124.0, -114.0)


# Here begins the form section
with st.form("prediction_form"):
    # Creating two columns for input fields
    col1, col2 = st.columns(2)

    with col1:
        median_income = st.number_input('Median Income', *median_income_range,
                                        value=st.session_state.median_income,
                                        step=0.1,
                                        help="Measured in tens of thousands. Ex. '3' for $30,000.")

        housing_median_age = st.slider('Median Age of Houses',
                                       *housing_median_age_range,
                                       value=st.session_state.housing_median_age,
                                       help="Median age of houses within a block.")

        total_rooms = st.number_input('Total Rooms',
                                      *total_rooms_range,
                                      value=st.session_state.total_rooms,
                                      help="Total number of rooms within a block.")

        total_bedrooms = st.number_input('Total Bedrooms',
                                         *total_bedrooms_range,
                                         value=st.session_state.total_bedrooms,
                                         help="Total number of bedrooms within a block.")
    with col2:
        population = st.number_input('Population',
                                     *population_range,
                                     value=st.session_state.population,
                                     help="Total population within a block.")

        households = st.number_input('Households',
                                     *households_range,
                                     value=st.session_state.households,
                                     help="Number of households within a block.")

        latitude = st.number_input('Latitude',
                                   *latitude_range,
                                   value=st.session_state.latitude,
                                   format="%.2f",
                                   help="Latitude of the block ranges from 32.0 to 42.0.")

        longitude = st.number_input('Longitude',
                                    *longitude_range,
                                    value=st.session_state.longitude,
                                    format="%.2f",
                                    help="Longitude of the block ranges from -124.0 to -114.0.")

        ocean_proximity = st.selectbox('Proximity to the Ocean',
                                       options=['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'],
                                       index=['<1H OCEAN',
                                              'INLAND',
                                              'NEAR OCEAN',
                                              'NEAR BAY',
                                              'ISLAND'].index(st.session_state.ocean_proximity),
                                       help="Proximity to the ocean can affect house prices.")

    # Button to submit the form
    submit_button = st.form_submit_button("Predict :rocket:")
# Handling form submission
if submit_button:
    # Collecting user inputs with the collect_inputs function
    collect_inputs()

    input_df = pd.DataFrame.from_dict({key: [value] for key, value in st.session_state['input_data'].items()})

    # Using the engineered features function for prediction
    input_df = add_engineered_features(input_df)

    errors = validate_inputs(input_df)  # Checking for input validation errors
    if errors:
        for error in errors:
            st.error(error)
    else:
        # If no errors are found continuing to perform the prediction
        predicted_price, error_message = predict_price(input_df)
        if error_message:
            st.error(f"Prediction error: {error_message}")
        else:
            st.success(f'The predicted median house price is ${predicted_price:,.2f}.')

# Here we use the reset inputs function as a button
# Reset button to reset inputs to default values
if st.button("Reset"):
    reset_inputs()
    st.rerun()  # st.rerun() used to refresh the page with default values

# Providing instructions and guidance for the user
st.markdown("### Instructions")
st.write("Fill in the fields based on the characteristics of a district in California and click "
         "'Predict' to see the model's prediction.")

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
