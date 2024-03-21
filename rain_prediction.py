import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import requests

# Load the data
data = pd.read_csv("combined_data.csv")

# Filter data for the year 2023
data_2023 = data[data['YEAR'] == '2023']

# Load the trained LSTM model
model = load_model('model3.keras')

columns = ['YEAR', 'MO', 'DY','ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'WS2M', 'T2M_MAX', 'T2M_MIN', 'T2MDEW', 'QV2M', 'PRECTOTCORR', 'PS', 'WD10M', 'WS10M_MAX', 'WS10M_MIN']

# converting to numeric
data_2023[columns] = data_2023[columns].apply(pd.to_numeric, errors='coerce')
data_2023['City'] = data_2023['City'].astype('category').cat.codes

# Exclude the target variable from the features
features = ['MO', 'DY', 'ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'WS2M', 'T2M_MAX', 'T2M_MIN', 'T2MDEW', 'QV2M',
            'PS', 'WD10M', 'WS10M_MAX', 'WS10M_MIN','City']

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(data_2023[features].values)
y = data_2023['PRECTOTCORR'].values

# Reshape the input data to be 3D [samples, timesteps, features] as required by LSTM
X = np.reshape(X, (X.shape[0], 1, X.shape[1]))

# Predictions
predictions = model.predict(X)

def run_predictionpage():
    st.title('Predictions for Precipitation in Mumbai (Year 2023)')

    # dataset
    st.write("### Dataset (Year 2023)")
    st.write(data_2023)

    #actual vs predicted precipitation 
    st.write("### Actual vs Predicted Precipitation (Year 2023)")
    index = range(len(data_2023))
    actual_predicted_df = pd.DataFrame({'Actual': y, 'Predicted': predictions.flatten()}, index=index)
    st.line_chart(actual_predicted_df)
      
    # Show a sample of the predictions
    st.write("### Predicted Values (Year 2023)")
    st.write(actual_predicted_df.head(100))
    
    predictions_df = pd.DataFrame({'Actual': y, 'Predicted': predictions.flatten()})
    st.write("### Actual vs Predicted Precipitation (Area Chart) (Year 2023)")
    st.area_chart(predictions_df)
    
    
    city = st.text_input("Enter the Name of the City")   
    
    # #API Keys
    weather_api_key = "556105f4f5f06239d40c226b2f11b769"
    # button to fetch and display weather data
    submit = st.button("Get Weather")
    if submit:
        st.title("Prediction for " + city + " is:")
        with st.spinner('Predicting the weather ...'):
            weather_data = get_weather_data(city, weather_api_key)
            st.text(f"{weather_data['main']['temp'] - 273.15:.2f}C")
            temp = weather_data['main']['temp'] - 273.15
            temp_min = weather_data['main']['temp_min'] 
            temp_max = weather_data['main']['temp_max'] 
            pressure = weather_data['main']['pressure'] 
            humidity = weather_data['main']['humidity'] 
            visiblity = weather_data['visiblity'] 
            wind_speed = weather_data['wind']['speed'] 
            wind_deg = weather_data['wind']['deg'] 
            cloud = weather_data['main']['temp'] 
    
    
    
    
    
    
    
    
    
    
def get_weather_data(city,weather_api_key):
   base_url = "http://api.openweathermap.org/data/2.5/weather?"
   complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
   response = requests.get(complete_url)
   st.write("API Response:", response.json())  # Debugging output
   return response.json()    
    


    
    
    
    
    
if __name__ == "__main__":
    run_predictionpage() 
