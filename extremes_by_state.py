# Import libraries
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from config import ow_api_key, zip_api_key

'''
        TODO
        - Write a function that returns the temperature in fahrenheit of a ZIP code
        - Give user a table of usable state abbreviations (WEB SCRAPE)
        - Get all ZIP codes from input state (ZIP API)
        - Let user see the warmest and coldest ZIP codes (OW API)
        - Print any weather alerts for warmest and coldest ZIP codes. (GOV API) 
'''

def main():

    print("\n\tMOST EXTREME WEATHER BY U.S. STATE")

    state_abbrv = input('\n\tSearch State By Abbreviation (Ex: AK, CA, CO, MD): ')

if __name__ == '__main__':
    main()