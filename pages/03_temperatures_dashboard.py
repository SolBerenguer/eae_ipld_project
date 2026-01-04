# the libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries for date conversions and build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about the daily temperatures of 10 cities around the world, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities (with some cleaning and modifications).")


# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/cities_temperatures.csv"

    temps_df = pd.read_csv(data_path)

    if temps_df is not None:
        temps_df["Date"] = pd.to_datetime(temps_df["Date"]).dt.date

    return temps_df


temps_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)


# ----- Data transformation -----

temps_df["AvgTemperatureCelsius"] = (temps_df["AvgTemperatureFahrenheit"] - 32) * 5 / 9


# ----- Extracting some basic information from the dataset -----

unique_countries_list = temps_df["City"].unique().tolist()

min_date = temps_df["Date"].min()
max_date = temps_df["Date"].max()

min_temp = temps_df["AvgTemperatureCelsius"].min()
max_temp = temps_df["AvgTemperatureCelsius"].max()

min_row = temps_df[temps_df["AvgTemperatureCelsius"] == min_temp].iloc[0]
max_row = temps_df[temps_df["AvgTemperatureCelsius"] == max_temp].iloc[0]

min_temp_city = min_row["City"]
min_temp_date = min_row["Date"]

max_temp_city = max_row["City"]
max_temp_date = max_row["Date"]


# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])
cols1[0].dataframe(pd.Series(unique_countries_list, name="Cities"), width="content")

cols1[2].write("#")

cols1[2].write(f"""
### ☃️ Min Temperature: {min_temp:.1f}°C
*{min_temp_city} on {min_temp_date}*
""")

cols1[2].write("#")

cols1[2].write(f"""
### 🏜️ Max Temperature: {max_temp:.1f}°C
*{max_temp_city} on {max_temp_date}*
""")


# ----- Plotting the temperatures over time for the selected cities -----

st.write("##")
st.header("Comparing the Temperatures of the Cities")

selected_cities = st.multiselect(
    "Select the cities to compare:",
    unique_countries_list,
    default=["Buenos Aires", "Dakar"],
    max_selections=4
)

cols2 = st.columns([6, 1, 6])

start_date = cols2[0].date_input(
    "Select the start date:",
    pd.to_datetime("2009-01-01").date()
)

end_date = cols2[2].date_input(
    "Select the end date:",
    pd.to_datetime("2018-12-31").date()
)

