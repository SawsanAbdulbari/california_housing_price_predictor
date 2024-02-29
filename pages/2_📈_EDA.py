import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


st.title(":chart_with_upwards_trend: Exploratory Data Analysis")

image = "img.png"
st.sidebar.image(image, caption='Image', use_column_width=True)
df = pd.read_csv("housing.csv")
st.sidebar.write("Final project for Python Machine Learning Diploma📊📈")
st.sidebar.write("")

# Creating and defining a filter for Geographical Distribution figure
st.sidebar.title('Filter Geographical Distribution')
st.sidebar.write("Filter figure with desired median house value range")
min_value = st.sidebar.slider('Minimum',
                              min_value=int(df['median_house_value'].min()),
                              max_value=int(df['median_house_value'].max()),
                              value=int(df['median_house_value'].min()))
max_value = st.sidebar.slider('Maximum',
                              min_value=int(df['median_house_value'].min()),
                              max_value=int(df['median_house_value'].max()),
                              value=int(df['median_house_value'].max()))
st.sidebar.write("")


# Signature
st.sidebar.write("")
st.sidebar.markdown("Made with :green_heart: by"
                    " Eng. [Sawsan Abdulbari](https://www.linkedin.com/in/sawsan-abdulbari-5a4533104)")


# Filtering the dataframe based on the slider's values
filtered_df = df[(df['median_house_value'] >= min_value) & (df['median_house_value'] <= max_value)]
# Displaying the number of properties matching the filter criteria
st.write("")
st.write(f"Number of properties matching criteria: {len(filtered_df)}")


# Creating a Plotly figure with the filtered DataFrame
fig = px.scatter(filtered_df,
                 x='longitude',
                 y='latitude',
                 color='median_house_value',
                 color_continuous_scale='Jet',
                 title='Geographical Distribution of Median House Values (Filtered)',
                 size_max=5,
                 height=400,
                 width=800,
                 labels={'median_house_value': 'Median House Value'})

# Adjusting the layout
fig.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 30},
                  coloraxis_colorbar=dict(title='Median House Value'))

# Displaying the figure in the Streamlit app
st.plotly_chart(fig)

# Displaying a filtered DataFrame example
filtered_df = df.iloc[:500, :].copy()

with st.expander("View Data"):
    # Displaying a styled subset of the filtered dataframe
    st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

    # Providing an option for user to download the original DataSet
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label='Download Data',
                       data=csv,
                       file_name="Data.csv",
                       mime="text/csv")


# Dividing median income in to appropriate bins for three map
df['income_bracket'] = pd.cut(df['median_income'],
                              bins=[0, 1.5, 3.0, 4.5, 6.0, np.inf],
                              labels=['Low',
                                      'Below Average',
                                      'Average',
                                      'Above Average',
                                      'High'])

# Dividing median age in to appropriate bins for three map
df['age_bracket'] = pd.cut(df['housing_median_age'],
                           bins=[0, 10, 20, 30, 40, 50,
                                 np.inf],
                           labels=['<10',
                                   '10-20',
                                   '20-30',
                                   '30-40',
                                   '40-50',
                                   '>50'])

# Ensuring that ocean_proximity, income_bracket and age_bracket are strings for Plotly to process them correctly
df['ocean_proximity'] = df['ocean_proximity'].astype(str)
df['income_bracket'] = df['income_bracket'].astype(str)
df['age_bracket'] = df['age_bracket'].astype(str)


# Creating the treemap figure
fig1 = px.treemap(df,
                  path=['ocean_proximity', 'income_bracket', 'age_bracket'],
                  values="median_house_value",
                  hover_data=["median_house_value"],
                  color="median_house_value",
                  color_continuous_scale='rdylbu',
                  title="Treemap of Housing Units by Ocean Proximity, Income Bracket, and Age Bracket")

# Customizing the layout
fig1.update_layout(
        width=800,
        height=650,
        margin=dict(l=0, r=0, b=0, t=30))

# Adding more interactivity
fig1.update_traces(
        hoverinfo="label+value+percent parent",
        textinfo="label+value")

# Displaying the figure in Streamlit
st.plotly_chart(fig1, use_container_width=True)

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
<p>Developed with <span style='color:red;'>❤</span> by <a href="https://www.linkedin.com/in/your-linkedin-id" target="_blank">Sawsan Abdulbari</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
