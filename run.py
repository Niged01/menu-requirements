import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('menu_requirements')

def get_passenger_numbers_data():
    """
    Get passenger numbers from User
    """
    print("Please enter flight number and number of passengers")
    print("Enter flight number bis class passenger and crew numbers, seperated by commas.")
    print("Example: LI300,50,140,10\n")

    input_str = input("Enter your data here: ")
    print(f"The data provided is {input_str}")


get_passenger_numbers_data()