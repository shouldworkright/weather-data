# Import libraries
import re
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from config import ow_api_key, zip_api_key

# Prints OpenWeather API data for a specified U.S. city
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
        location_name = data["name"]
        country_name = iso_to_fullname(data["sys"]["country"])  # 2-letter ISO string converted to country's full name

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
        print("\n\tLocation: " +
              str(location_name) +
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

# Prints OpenWeather API data for a specified U.S. ZIP code
def zip_data(zip_code):

    # Base URL for API access
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Append data to URL
    complete_url = base_url + "?zip=" + zip_code + ",us&units=imperial&appid=" + ow_api_key

    # Pull data from OpenWeather API for specified city
    response = requests.get(complete_url)

    # Convert JSON data to a Python-readable dictionary
    data = response.json()

    if data["cod"] != "404":

        # Grab city name and country name from API
        location_name = data["name"]
        country_name = iso_to_fullname(data["sys"]["country"])  # 2-letter ISO string converted to country's full name

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
        print("\n\tLocation: " +
              str(location_name) +
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
        print("\n\tERROR: Location Not Found")

# Returns a country's full name as a string when passed a 2 letter ISO 3166-1 Alpha-2 country code
def iso_to_fullname(user_iso_code):

    # URL for web-scraping text data
    url = "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements"

    # Fetch and parse raw HTML content from the URL
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html5lib")

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

# Returns a pair of latitude-longitude coordinates as a string given a ZIP code
def zip_to_coord(zip_code):

    # For debugging purposes. Used to identify the ZIP code being passed.
    # print(zip_code)

    # Grab data from file containing ZIP codes and corresponding coordinates
    data = pd.read_excel("us-zip-code-latitude-and-longitude.xlsx", converters={"Zip": lambda x: str(x)})
    df = pd.DataFrame(data)

    # Initialize coordinate values
    latitude, longitude = "0", "0"

    for index, row in df.iterrows():

        # If user-entered ZIP code matches one that exists, find its latitude and longitude
        if df.loc[index, "Zip"] == zip_code:
            latitude = str(df.loc[index, "Latitude"])
            longitude = str(df.loc[index, "Longitude"])
            return latitude, longitude

        # For debugging purposes. Replace "int" with upper bound of desired
        # ZIP code range to stop program from reading all ZIP codes in .xlsx file.
        # Used when function can't find data for a specific ZIP code.
        # Use this link to find all zip codes for a specific state:
        # https://www.zipcodestogo.com/ZIP-Codes-by-State.htm

        '''
        if index > int:
            print("Why can't I find that ZIP code?")
            return
        '''

# Returns all ZIP codes for a U.S. state as an array when passed the state's 2-letter abbreviation
def get_zips(state_abbrev):

    # Base URL for API access
    complete_url = "https://api.zip-codes.com/ZipCodesAPI.svc/1.0/GetAllZipCodes?state="\
               + state_abbrev + "&country=US&key=" + zip_api_key

    # Pull data from ZIP Code API for specified city
    response = requests.get(complete_url)

    # Fetch all ZIP codes as an array
    zip_codes = response.json()

    return zip_codes

# Prints a list of all U.S. state abbreviations
def all_state_abbrevs():

    # URL for web-scraping text data
    url = "https://simple.wikipedia.org/wiki/U.S._postal_abbreviations"

    # Fetch and parse raw HTML content from the URL
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html5lib")

    # Get table of states and abbreviations from HTML content
    table = soup.find_all("table")[0]

    # Get all rows from the table
    table_data = table.find_all("tr")

    # Print all searchable state abbreviations
    for row in table_data:

        # Get cells from current table row
        cells = row.findAll("td")

        # Skips initial row of table
        if len(cells) == 2:
            state_abbrev = cells[0].text.strip()  # 2-letter state abbreviation
            state_full = cells[1].text.strip()  # Full state name

            print("\t" + state_abbrev + " -> " + state_full)

    return

# Returns true if passed abbreviation belongs to a U.S. state
def state_abbrev_check(state_abbrev):

    # URL for web-scraping text data
    url = "https://simple.wikipedia.org/wiki/U.S._postal_abbreviations"

    # Fetch and parse raw HTML content from the URL
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html5lib")

    # Get table of states and abbreviations from HTML content
    table = soup.find_all("table")[0]

    # Get all rows from the table
    table_data = table.find_all("tr")

    # Initialize current state abbreviation being pulled from the web page
    state_abbrev_web = ""

    for row in table_data:

        # Get cells from current table row
        cells = row.findAll("td")

        # Get 2-letter state abbreviation from current row
        if len(cells) == 2:
            state_abbrev_web = cells[0].text.strip()

        # If there is a match, return True
        if state_abbrev_web == state_abbrev:
            return True

    return False

# Returns name and temperature of a ZIP code
def name_and_temp(zip_code):

    # Base URL for API access
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Append data to URL
    complete_url = base_url + "?zip=" + zip_code + ",us&units=imperial&appid=" + ow_api_key

    # Pull data from OpenWeather API for specified city
    response = requests.get(complete_url)

    # Convert JSON data to a Python-readable dictionary
    data = response.json()

    # Initialize location name and temperature
    zip_name, current_temp = "", 0

    if data["cod"] != "404":

        # Grab name of ZIP code
        zip_name = data["name"]

        # Pull relevant data from "main" key
        main = data["main"]
        current_temp = main["temp"]  # Current temperature

    else:
        print("\n\tERROR: ZIP Code Not Found")

    return zip_name, current_temp

# Prints weather forecast for a given pair of latitude-longitude coordinates
def geo_forecast(latitude, longitude):

    # For debugging purposes. Used to identify the coordinates being passed.
    # print(latitude + ", " + longitude)

    # URL for base API access
    base_url = "https://api.weather.gov/points/" + str(latitude) + "," + str(longitude)

    # Pull data from National Weather Service API for specified coordinates
    response = requests.get(base_url)
    data = response.json()

    # If an error code returns as part of the API request, print this message and return
    if "status" in data:
        print("\n\tNo forecast data is available for this location.")
        return

    # Contains url for weather forecast
    forecast_url = data["properties"]["forecast"]

    # If no weather forecast exists, print this message and return
    if forecast_url == None:
        print("\n\tNo forecast data is available for this location.")
        return

    # Pull forecast data for specified location
    response = requests.get(forecast_url)
    data = response.json()

    # Pull forecast summary from API
    forecast = data["properties"]["periods"][0]["detailedForecast"]
    print("\n\tWEATHER FORECAST:")
    print("\t" + forecast)

def main():

    print("\n\tMOST EXTREME WEATHER BY U.S. STATE")
    print("\n\tSearchable States:")
    all_state_abbrevs()

    # Prompt user to enter search a state
    while True:
        state_abbrev = input("\n\tSearch State By Abbreviation: ")
        state_abbrev = state_abbrev.upper()
        state_abbrev_match = re.match("[A-Za-z]{2}", state_abbrev)

        # Check for valid user input
        if state_abbrev_match == None:
            print("\n\tERROR: Please select a valid state.")
        elif state_abbrev_check(state_abbrev) == False:
            print("\n\tERROR: Please select a valid state.")
        else:
            break

    # Create an array of all ZIP codes for user-input state
    zip_codes = get_zips(state_abbrev)

    # Initialize hottest and coldest location values
    hottest_zip, coldest_zip = 0, 0
    hottest_temp, coldest_temp = 0, 0
    hottest_name, coldest_name = "", ""

    # Control variable for FOR loop
    search_num = 0

    for zip in zip_codes:

        curr_name, curr_temp = name_and_temp(zip)
        search_num += 1

        # Skip any ZIP codes that don't return data from OpenWeather API
        if curr_name == "" and curr_temp == 0:
            continue

        # First loop iteration sets the coldest temperature among all ZIP codes
        if search_num == 1:
            coldest_zip = zip
            coldest_temp = curr_temp
            coldest_name = curr_name

        # Set values for current hottest location
        if curr_temp > hottest_temp:
            hottest_zip = zip
            hottest_temp = curr_temp
            hottest_name = curr_name

        # Set values for current coldest location
        if curr_temp < coldest_temp:
            coldest_zip = zip
            coldest_temp = curr_temp
            coldest_name = curr_name

        print("\n\tSearching ZIP Code " + str(search_num) + "/" + str(len(zip_codes)))

    print("\n\t----------------------------------------------------------------------------------")

    # Print OpenWeather API data for hottest location
    print("\n\tHOTTEST LOCATION IN " + state_abbrev)
    zip_data(hottest_zip)

    # Print National Weather Service forecast for hottest location
    hottest_zip = hottest_zip.lstrip("0")    # Strip leading zeroes to interface with NWS API
    latitude, longitude = zip_to_coord(hottest_zip)
    geo_forecast(latitude, longitude)

    print("\n\t----------------------------------------------------------------------------------")

    # Print OpenWeather API data for coldest location
    print("\n\tCOLDEST LOCATION IN " + state_abbrev)
    zip_data(coldest_zip)

    # Print National Weather Service forecast for coldest location
    coldest_zip = coldest_zip.lstrip("0")    # Strip leading zeroes to interface with NWS API
    latitude, longitude = zip_to_coord(coldest_zip)
    geo_forecast(latitude, longitude)

    print("\n\t----------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()