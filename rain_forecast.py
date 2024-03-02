import streamlit as st
import requests


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
        
        
if __name__ == "__main__":
    run_weather_forecast()        