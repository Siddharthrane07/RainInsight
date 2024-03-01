import streamlit as st
import requests
import subprocess
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from streamlit_option_menu import option_menu

# Load the data
data = pd.read_csv("mumbai.csv")

# Load the trained LSTM model
model = load_model('model1.keras')

# Exclude the target variable from the features
features = ['MO', 'DY', 'ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'WS2M', 'T2M_MAX', 'T2M_MIN', 'T2MDEW', 'QV2M',
            'PS', 'WD10M', 'WS10M_MAX', 'WS10M_MIN']

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(data[features].values)
y = data['PRECTOTCORR'].values

# Reshape the input data to be 3D [samples, timesteps, features] as required by LSTM
X = np.reshape(X, (X.shape[0], 1, X.shape[1]))

# Predictions
predictions = model.predict(X)


def get_weather_data(city,weather_api_key):
   base_url = "http://api.openweathermap.org/data/2.5/weather?"
   complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
   response = requests.get(complete_url)
   return response.json()

def run_weather_forecast():
    
    st.title("Weather Forecasting with LLM")
    city = st.text_input("Enter city name", "London")

    # #API Keys
    weather_api_key = "556105f4f5f06239d40c226b2f11b769"

    # button to fetch and display weather data
    submit = st.button("Get Weather")

    if submit:
        st.title("Weather Updates for " + city + " is:")
        with st.spinner('Fetching weather data...'):
            weather_data = get_weather_data(city, weather_api_key)
           

            #if the city is found 
            if weather_data.get("cod") != 404:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature 🌡", f"{weather_data['main']['temp'] - 273.15:.2f}C")
                    st.metric("Humidity 💧", f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric("Pressure 💨", f"{weather_data['main']['pressure']}hPa")
                    st.metric("Wind Speed 🍃", f"{weather_data['wind']['speed']}m/s")
        
def run_predictionpage():
    st.title('Predictions for Precipitation in Mumbai')

    # dataset
    st.write("### Dataset")
    st.write(data)

    #actual vs predicted precipitation 
    st.write("### Actual vs Predicted Precipitation")
    index = range(len(data))
    actual_predicted_df = pd.DataFrame({'Actual': y, 'Predicted': predictions.flatten()}, index=index)
    st.line_chart(actual_predicted_df)
      
    # Show a sample of the predictions
    st.write("### Predicted Values")
    st.write(actual_predicted_df.head(100))
    
    predictions_df = pd.DataFrame({'Actual': y, 'Predicted': predictions.flatten()})
    st.write("### Actual vs Predicted Precipitation (Area Chart)")
    st.area_chart(predictions_df)


def run_apps():

   with st.sidebar:
# Sidebar configuration
    st.sidebar.title("Main Menu")

# the options
    options = ["Weather Forecast","Precipitation Predictions"]

# Selectbox for menu 
    selected = option_menu(
      menu_title="Select an option",
      options=options,
    #   icons=["weather", "rain"],
      menu_icon="cast",
      default_index = 0,
    #   orientation = "horizontal"
    )

   if selected == "Weather Forecast":
       run_weather_forecast()
   elif selected == "Precipitation Predictions":
           run_predictionpage()


run_apps()









#/home/codespace/.local/lib/python3.10/site-packages/bin/streamlit run demo.py
