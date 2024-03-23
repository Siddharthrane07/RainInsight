from ossaudiodev import openmixer
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry

# # Load the data
# data = pd.read_csv("combined_data.csv")

# # Filter data for the year 2023
# data_2023 = data[data['YEAR'] == '2023']

# # Load the trained LSTM model
# model = load_model('model3.keras')

# columns = ['YEAR', 'MO', 'DY','ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'WS2M', 'T2M_MAX', 'T2M_MIN', 'T2MDEW', 'QV2M', 'PRECTOTCORR', 'PS', 'WD10M', 'WS10M_MAX', 'WS10M_MIN']

# # converting to numeric
# data_2023[columns] = data_2023[columns].apply(pd.to_numeric, errors='coerce')
# data_2023['City'] = data_2023['City'].astype('category').cat.codes

# # Exclude the target variable from the features
# features = ['MO', 'DY', 'ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'WS2M', 'T2M_MAX', 'T2M_MIN', 'T2MDEW', 'QV2M',
#             'PS', 'WD10M', 'WS10M_MAX', 'WS10M_MIN','City']

# # Normalize the data
# scaler = MinMaxScaler(feature_range=(0, 1))
# X = scaler.fit_transform(data_2023[features].values)
# y = data_2023['PRECTOTCORR'].values

# # Reshape the input data to be 3D [samples, timesteps, features] as required by LSTM
# X = np.reshape(X, (X.shape[0], 1, X.shape[1]))

# # Predictions
# predictions = model.predict(X)

def run_predictionpage():
    # st.title('Predictions for Precipitation in Mumbai (Year 2023)')

    # # dataset
    # st.write("### Dataset (Year 2023)")
    # st.write(data_2023)

    # #actual vs predicted precipitation 
    # st.write("### Actual vs Predicted Precipitation (Year 2023)")
    # index = range(len(data_2023))
    # actual_predicted_df = pd.DataFrame({'Actual': y, 'Predicted': predictions.flatten()}, index=index)
    # st.line_chart(actual_predicted_df)
    
    # # Show a sample of the predictions
    # st.write("### Predicted Values (Year 2023)")
    # st.write(actual_predicted_df.head(100))
    
    # predictions_df = pd.DataFrame({'Actual': y, 'Predicted': predictions.flatten()})
    # st.write("### Actual vs Predicted Precipitation (Area Chart) (Year 2023)")
    # st.area_chart(predictions_df)
    
    
    city = st.text_input("Enter the Name of the City")   
    
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    weather_api_key = "556105f4f5f06239d40c226b2f11b769"
    
    # button to fetch and display weather data
    submit = st.button("Get Weather")
    if submit:
        # st.title("Prediction for " + city + " is:")
        with st.spinner('Getting details ...'):
            weather_data = get_weather_data(city, weather_api_key)
            
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            x = get_current_weather_data(lat,lon,openmeteo)
            
            y = get_past_weather_data(lat,lon,openmeteo)
        
            
            df = pd.DataFrame(y)
            
            df['date'] = pd.to_datetime(df['date'])
            
            df = df.set_index('date')
            
            
            st.title("Past 15 days Precipitation")
            st.line_chart(df)
            st.bar_chart(df)
            st.area_chart(df)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
def get_current_weather_data(lat,lon,openmeteo):
   
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "rain", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "timezone": "GMT"
    }
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_rain = current.Variables(3).Value()
    current_cloud_cover = current.Variables(4).Value()
    current_pressure_msl = current.Variables(5).Value()
    current_surface_pressure = current.Variables(6).Value()
    current_wind_speed_10m = current.Variables(7).Value()
    current_wind_direction_10m = current.Variables(8).Value()
    current_wind_gusts_10m = current.Variables(9).Value()
    
    return current_apparent_temperature
    
    
    
    
def get_past_weather_data(lat,lon,openmeteo):
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": lat,
	"longitude": lon,
	"daily": "precipitation_sum",
	"timezone": "GMT",
	"past_days": 15,
	"forecast_days": 0
    }
    
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    daily = response.Daily()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    # st.write(daily_data["date"])
    dates_with_time = pd.to_datetime(daily_data["date"])
    dates = [date.strftime("%Y-%m-%d") for date in dates_with_time]
    
    daily_precipitation_sum = daily.Variables(0).ValuesAsNumpy()
    
    past_data = {"date":dates,"precipitation":daily_precipitation_sum}
    
    return past_data  

    
def get_weather_data(city,weather_api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()    
    


    
    
    
    
    
if __name__ == "__main__":
    run_predictionpage() 
