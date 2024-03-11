import folium
import requests
import streamlit as st
from streamlit_folium import folium_static
import leafmap.foliumap as leafmap

def get_weather_data(city,weather_api_key):
   base_url = "http://api.openweathermap.org/data/2.5/weather?"
   complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
   response = requests.get(complete_url)
   st.write("API Response:", response.json())  # Debugging output
   return response.json()


def run_weather_forecast():
    tab1, tab2, tab3 = st.tabs(["Weather", "Map", "visuals"])
    
    with tab1:
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
                        
    with tab2:
         st.title("Rain Prediction Map")
 
         # Get user input for city and API key
         city = st.text_input("Enter city name", "")


         # Fetch weather data when button is clicked
         if st.button("Fetch Weather"):
              weather_data = get_weather_data(city, weather_api_key)

              if weather_data:
                 st.write("Weather Data:", weather_data)  # Debugging statement
                 # Extract relevant information from weather data
                 latitude = weather_data["coord"]["lat"]
                 longitude = weather_data["coord"]["lon"]
                 rain_prediction = weather_data.get("rain", {}).get("1h", 0)

                 # Create a map centered at the city's coordinates
                 m = folium.Map(location=[latitude, longitude], zoom_start=10)

                 folium.Marker(location=[latitude, longitude],
                 popup=f"{city}: Rain Prediction - {rain_prediction} mm/h").add_to(m)
                 
                 m.add_heatmap(
                    df,
                    latitude="lat",
                    longitude="lon",
                    value="quant_feature",
                    name="Heat map",
                    radius=20,
                )
                 m.add_xy_data(df2, 
                 x='consolidated_longitude',
                 y='consolidated_latitude',
                 layer_name='Marker cluster')
                 m.to_streamlit()
                 folium_static(m)
              else:
                 st.error("Failed to fetch weather data. Please check the city name and try again.")

        
            #    mapObj = folium.Map(location=[19.7515, 75.7139],zoom_start=7) 
    #    st.components.v1.html(open("mapObj", "r").read(), width=800, height=600)
    #    mapObj.save('output.html')
    #     st.title("Weather Updates for " + city + " is:")
    #     mapObj = folium.Map(location=[21.437730075416685, 77.255859375],
    #     zoom_start=2, tiles='OpenStreetMap')
    #     st.title("Weather Updates for " + city + " is:")
        # import folium
        # st.title("Weather Updates for " + city + " is:")
        # mapObj = folium.Map(location=[19.7515, 75.7139], zoom_start=7)  # zoom_control=False - for no zoom
 
        

        
        
if __name__ == "__main__":
    run_weather_forecast()        