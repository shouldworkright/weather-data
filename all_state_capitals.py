# Import libraries
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from config import ow_api_key

# Prints OpenWeather API data for a specified city
def city_data(city_name):

    # Base URL for API access
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Append data to URL
    complete_url = base_url + "?q=" + city_name + ",us&units=imperial&appid=" + ow_api_key

    # Pull data from OpenWeather API for specified city
    response = requests.get(complete_url)

    # Convert JSON data to a Python-readable dictionary
    data = response.json()

    if data["cod"] != "404":

        # Grab city name and country name from API
        city_name = data["name"]
        country_name = iso_conversion(data["sys"]["country"])  # 2-letter ISO string converted to country's full name

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
              "\n\tCountry: " +
              str(country_name) +
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

# Returns a country's full name as a string when passed a 2 letter ISO 3166-1 Alpha-2 country code
def iso_conversion(user_iso_code):

    # URL for web-scraping text data
    url = "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements"

    # Fetch and parse raw HTML content from the URL
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html5lib')

    # Get the second table from the HTML file
    table = soup.find_all("table")[2]

    # Get all rows from the table
    table_data = table.findChildren("tr")

    for row in table_data:

        # Get cells from current table row
        cells = row.findAll("td")

        # Only search rows that have cells
        if len(cells) > 0:

            # Get ISO code and full name of corresponding country
            web_iso_code = cells[0].text.strip()
            country = cells[1].text.strip()

            # If user-input ISO code has a match, return the country's full name
            if user_iso_code == web_iso_code:
                return country

def main():

    print("\n\tCURRENT WEATHER DATA FOR ALL 50 U.S. STATE CAPITALS")

    # URL for web-scraping text data
    url = "https://en.wikipedia.org/wiki/List_of_capitals_in_the_United_States"

    # Fetch raw HTML content from the url
    html_content = requests.get(url).text

    # Parse the raw HTML content
    soup = BeautifulSoup(html_content, 'html5lib')

    # Get the second table from the HTML content
    table = soup.find_all('table')[1]

    # Get all rows from the table
    table_data = table.find_all('tr')

    # Request weather data from each
    for row in table_data:

        # Get state capital from current row
        row_data = row.find_all('th')
        state_capital = row_data[0].get_text(strip=True)  # Strip newlines and spaces from string

        # Skip header and footer row
        if ((state_capital == 'State') or (state_capital == '[19]')):
            continue

        city_data(state_capital)

if __name__ == '__main__':
    main()
