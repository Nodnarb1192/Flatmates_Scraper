from datetime import datetime
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread
import os
import json


def scrape_data(suburb, postcode):
    """
    Scrapes data from the given URL and returns average room rent, people looking, rooms offered, and supply-demand data.
    """
    # Reformat suburb to be lowercase and replace spaces with hyphens
    suburb = suburb.lower().replace(" ", "-")
    # Convert postcode to string
    postcode = str(postcode)
    url = f"https://flatmates.com.au/value-my-room/{suburb}-{postcode}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        # Extract average room rent
        average_rent = soup.find('span', class_='average-rent-number').text 
        
        # Extract supply and demand data
        supply_demand_data = soup.find_all('td', {'class': ['people-looking-chart', 'rooms-offered-chart']})
        people_looking = supply_demand_data[0].text
        rooms_offered = supply_demand_data[1].text
        supply_demand = f"{people_looking}:{rooms_offered}"

        # Extract time stamp
        time_stamp = datetime.now().strftime("%d/%m/%Y")

        # Convert suburb to title case and replace hyphens with spaces
        suburb = suburb.title().replace("-", " ")

        return suburb, postcode, average_rent, people_looking, rooms_offered, supply_demand, time_stamp
        
    except Exception as e:
        pass


def upload_to_sheets(data):
    """
    Uploads data to a Google Sheet.

    Args:
        data: A list of values to be added to the sheet.

    Returns:
        None
    """

    # Fetch credentials from environment variables
    creds_json = os.getenv('GSPREAD_CREDENTIALS')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    
    # Check if the sheet has header if not add the headers ["Average Rent", "People Looking", "Rooms Offered", "Supply and Demand Ratio"]
    if not sheet.row_values(1):
        sheet.append_row(["Suburb", "Postal Code", "Average Rent", "People Looking", "Rooms Offered", "Supply and Demand Ratio", "Time Stamp"])

    sheet.append_row(data)

if __name__ == "__main__":
    # Read australian_postcodes.xlsx and extract suburb and postcode
    df = pd.read_excel("australian_postcodes.xlsx")
    df['Postcode'] = df['Postcode'].apply(lambda x: '{0:0>4}'.format(x))
    suburb = df["Locality"].tolist()
    postcode = df["Postcode"].tolist()
    

    # make the suburb and postcode a dictionary with suburb:postcode as key:value pair
    suburb_postcode = dict(zip(suburb, postcode))
    # iterate over the dictionary and call the scrape_data function
    for suburb, postcode in suburb_postcode.items():
        result = scrape_data(suburb, postcode)
        if result:
            upload_to_sheets(result)
        else:
            pass
