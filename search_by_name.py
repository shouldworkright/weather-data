# Import libraries
import requests
from datetime import datetime
from config import api_key

def main():

    # Base URL for API access
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Prompt user to enter city name
    city_name = input("\n\tEnter city name: ")

    # Append data to URL
    complete_url = base_url + "?q=" + city_name + "&units=imperial&appid=" + api_key

    # Pull data from OpenWeather API for specified city
    response = requests.get(complete_url)

    # Convert JSON data to a Python-readable dictionary
    data = response.json()

    if data["cod"] != "404":

        # Grab city name from API
        city_name = data["name"]

        # Get the current date and time
        date = datetime.date(datetime.now())
        time = datetime.time(datetime.now())

        # Pull relevant data from "main" key
        main = data["main"]
        current_temp = main["temp"]  # Current temperature
        min_temp = main["temp_min"]  # Minimum temperature
        max_temp = main["temp_max"]  # Maximum temperature
        pressure = main["pressure"]  # Atmospheric pressure
        humidity = main["humidity"]  # Humidity percentage

        # Pull relevant data from "weather" key
        weather = data["weather"]
        weather_desc = weather[0]["description"]  # Description of weather

        # Print all data
        print("\n\tCity: " +
                str(city_name) +
              "\n\tDate: " +
                str(date) +
              "\n\tTime: " +
                str(time) +
              "\n\tWeather: " +
                str(weather_desc) +
              "\n\tCurrent Temperature (Farenheit): " +
                str(current_temp) +
              "\n\tHigh (Farenheit): " +
                str(max_temp) +
              "\n\tLow (Farenheit): " +
                str(min_temp) +
              "\n\tAtmospheric Pressure (hPa): " +
                str(pressure) +
              "\n\tHumidity (Percentage): " +
                str(humidity))

    else:
        print("\n\tERROR: City Not Found")

if __name__ == "__main__":
    main()