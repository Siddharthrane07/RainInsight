import requests
import streamlit as st
from streamlit_folium import folium_static
import folium
<<<<<<< HEAD
=======
import pydeck as pdk
import streamlit.components.v1 as components
from jinja2 import Template
>>>>>>> 7072a88 (made some chnages in prediction page)

API_KEY = "556105f4f5f06239d40c226b2f11b769"

def get_weather_data(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"  
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching weather data. Status code: {response.status_code}")
        return None
<<<<<<< HEAD

def display_weather_forecast(weather_data):
    if weather_data:
        # Extract relevant information from weather data
        latitude = weather_data["coord"]["lat"]
        longitude = weather_data["coord"]["lon"]

        # Create a map centered at the city's coordinates
        m = folium.Map(location=[latitude, longitude], zoom_start=10)
        pop_up_content = f"""
        <b>City:</b> {weather_data['name']}<br>
        <b>Country:</b> {weather_data['sys']['country']}<br>
        <b>Current Temperature:</b> {weather_data['main']['temp']}°C<br>
        <b>Weather:</b> {weather_data['weather'][0]['description'].capitalize()}
        """

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(folium.Html(pop_up_content, script=True)),
            icon=folium.Icon(color='blue')
        ).add_to(m)

        return m

=======

def display_weather_forecast(weather_data):
    if weather_data:
        # Extract relevant information from weather data
        latitude = weather_data["coord"]["lat"]
        longitude = weather_data["coord"]["lon"]

        # Create a map centered at the city's coordinates
        m = folium.Map(location=[latitude, longitude], zoom_start=10)
        pop_up_content = f"""
        <b>City:</b> {weather_data['name']}<br>
        <b>Country:</b> {weather_data['sys']['country']}<br>
        <b>Current Temperature:</b> {weather_data['main']['temp']}°C<br>
        <b>Weather:</b> {weather_data['weather'][0]['description'].capitalize()}
        """

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(folium.Html(pop_up_content, script=True)),
            icon=folium.Icon(color='blue')
        ).add_to(m)

        return m

def display_leaflet_weather_map(weather_data):
    if weather_data:
        # Assuming you've adjusted your HTML template as described
        with open("leaflet_rain_map.html", 'r', encoding='utf-8') as f:
            html_template_content = f.read()

        # Pre-process the template to replace Leaflet placeholders
        preprocessed_template = html_template_content.replace("{s}", "{{'{'}}s{{'}'}}").replace("{z}", "{{'{'}}z{{'}'}}").replace("{x}", "{{'{'}}x{{'}'}}").replace("{y}", "{{'{'}}y{{'}'}}")

        # Create a Jinja2 template
        template = Template(preprocessed_template)

        # Render the template with actual weather data
        html_filled = template.render(
            latitude=weather_data["coord"]["lat"],
            longitude=weather_data["coord"]["lon"],
            city=weather_data["name"],
            temperature=weather_data["main"]["temp"],
            humidity=weather_data["main"]["humidity"],
            pressure=weather_data["main"]["pressure"],
            wind_speed=weather_data["wind"]["speed"]
        )

        # Use Streamlit's components.html to render the filled HTML
        components.html(html_filled, height=600, scrolling=True)
    
    
>>>>>>> 7072a88 (made some chnages in prediction page)
def run_weather_forecast():
    tab1, tab2 = st.tabs(["Weather", "Map"])

    with tab1:
        st.title("Weather Forecasting with LLM")
        city = st.text_input("Enter city name", "London")
        submit = st.button("Get Weather")

        if submit:
            st.title(f"Weather Updates for {city}:")
            with st.spinner('Fetching weather data...'):
                weather_data = get_weather_data(city)
                if weather_data and weather_data.get("cod") != 404:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Temperature 🌡", f"{weather_data['main']['temp']}C")
                        st.metric("Humidity 💧", f"{weather_data['main']['humidity']}%")
                    with col2:
                        st.metric("Pressure 💨", f"{weather_data['main']['pressure']}hPa")
                        st.metric("Wind Speed 🍃", f"{weather_data['wind']['speed']}m/s")
                else:
                    st.error("City not found or API limit reached. Please try again.")

    with tab2:
        st.title("Rain Prediction Map")
        city = st.text_input("Enter a city name for the map", "")
<<<<<<< HEAD
=======

        if st.button("Show Map"):
            weather_data = get_weather_data(city)
            if weather_data:
                map_display = display_weather_forecast(weather_data)
                if map_display:
                    folium_static(map_display)
                else:
                    st.error("Failed to fetch weather data. Please check the city name and try again.")
                    
            # Display the Leaflet rain map
            display_leaflet_weather_map(weather_data)
>>>>>>> 7072a88 (made some chnages in prediction page)

        if st.button("Show Map"):
            weather_data = get_weather_data(city)
            if weather_data:
                map_display = display_weather_forecast(weather_data)
                if map_display:
                    folium_static(map_display)
                else:
                    st.error("Failed to fetch weather data. Please check the city name and try again.")

<<<<<<< HEAD
if __name__ == "__main__":
    run_weather_forecast()
=======
if __name__ == "_main_":
    run_weather_forecast()
>>>>>>> 7072a88 (made some chnages in prediction page)
