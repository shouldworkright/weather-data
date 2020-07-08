# Import libraries
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from config import api_key

def print_city_data(city_name):

    # Base URL for API access
    base_url = "http://api.openweathermap.org/data/2.5/weather"

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
        print("ERROR: City Not Found")

def main():

    print('\n\tCURRENT WEATHER DATA FOR ALL 50 U.S. STATE CAPITALS')

    # Base URL for API access
    url = "https://en.wikipedia.org/wiki/List_of_capitals_in_the_United_States"

    # Fetch raw HTML content from the url
    html_content = requests.get(url).text

    # Parse the raw HTML content
    soup = BeautifulSoup(html_content, 'html5lib')

    # Get the second table from the HTML content
    table = soup.find_all('table')[1]

    # Get all rows from the table
    table_data = table.find_all("tr")

    # Request weather data from each
    for row in table_data:

        # Get state capital from current row
        row_data = row.find_all('th')
        state_capital = row_data[0].get_text(strip=True)    # Strip newlines and spaces from string

        # Skip header and footer row
        if ((state_capital == 'State') or (state_capital == '[19]')):
            continue

        print_city_data(state_capital)

if __name__ == "__main__":
    main()