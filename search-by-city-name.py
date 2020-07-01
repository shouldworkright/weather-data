import requests
from config import api_key

# Base URL for API access
base_url = "http://api.openweathermap.org/data/2.5/weather"

# Prompt user to enter city name
city_name = input("Enter city name: ")

# Append data to URL
complete_url = base_url + "?q=" + city_name + "&units=imperial&appid=" + api_key

# Pull data from OpenWeather API for specified city
response = requests.get(complete_url)

# Convert JSON data to a Python-readable dictionary
data = response.json()

if data["cod"] != "404":

    # Store all data from "main" key in a variable
    main = data["main"]

    # Store all data from "weather" key in a variable
    weather = data["weather"]

    # Pull relevant data from "main" key
    current_temp = main["temp"]             # Current temperature
    min_temp = main["temp_min"]             # Minimum temperature
    max_temp = main["temp_max"]             # Maximum temperature
    pressure = main["pressure"]             # Atmospheric pressure
    humidity = main["humidity"]             # Humidity percentage

    # Pull relevant data from "weather" key
    weather_desc = weather[0]["description"]    # Description of weather

    # Print all data
    print("\n   Weather: " +
                str(weather_desc) +
          "\n   Current Temperature (Farenheit): " +
                str(current_temp) +
          "\n   High (Farenheit): " +
                str(max_temp) +
          "\n   Low (Farenheit): " +
                str(min_temp) +
          "\n   Atmospheric Pressure (hPa): " +
                str(pressure) +
          "\n   Humidity (Percentage): " +
                str(humidity))

else:
    print("ERROR: City Not Found")