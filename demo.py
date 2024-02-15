import streamlit as st
import requests
from openai import OpenAI

# Define your OpenAI API key
openai_api_key = "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"

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=openai_api_key)

# import numpy as np
# import pandas as pd

def get_weather_data(city,weather_api_key):
   base_url = "http://api.openweathermap.org/data/2.5/weather?"
   complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
   response = requests.get(complete_url)
   return response.json()

def generate_weather_description(data,openai_api_key):
   
   try:
      #convert temperature from kelvin to celsius
      temperature = data['main']['temp'] - 273.15
      description = data['weather'][0]['description']
      prompt = f"The current weather in your city is {description} with a temperature of {temperature:.1f}C . Explain this in a simple way for a general audience."
      
      response = client.completions.create(engine="gpt-3.5-turbo-instruct",
      prompt=prompt,
      max_tokens=60)
      
      return response.choices[0].txt.strip()
   except Exception as e:
      return str(e)

def main():
   # Sidebar configuration
    st.sidebar.title("Weather Forecasting with LLM")
    city = st.sidebar.text_input("Enter city name","London")
   
    # #API Keys
    weather_api_key = "556105f4f5f06239d40c226b2f11b769"
    openai_api_key = "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"
    
    #button to fetch and display weather data
    submit = st.sidebar.button("Get Weather")
    
    if submit:
      st.title("Weather Updates for " + city + " is:")
      with st.spinner('Fetching weather data...'):
         weather_data = get_weather_data(city,weather_api_key)
         print(weather_data)
         
         #check if the city is found and display weather data
         if weather_data.get("cod")!=404:
            col1,col2 = st.columns(2)
            with col1:
               st.metric("Temperature 🌡",f"{weather_data['main']['temp'] - 273.15:.2f}C")
               st.metric("Humidity 💧",f"{weather_data['main']['humidity']}%")
            with col2:
               st.metric("Pressure 💨", f"{weather_data['main']['pressure']}hPa")
               st.metric("Wind Speed 🍃",f"{weather_data['wind']['speed']}m/s")
               
            #Generate and display a frendly weather description
            weather_description = generate_weather_description(weather_data,openai_api_key)
            st.write(weather_description)
         else:
            #Display an error message if the city is not found            
            st.error("City not found or an error occured!")                              
                                                               
if __name__ == "__main__":
   main()
    
    