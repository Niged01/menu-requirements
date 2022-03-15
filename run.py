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
    while True:
        print("Please enter flight number and number of passengers")
        print("Enter flight number bis class passenger and crew numbers, seperated by commas.")
        print("Example: 300,50,140,10\n")

        input_str = input("Enter your data here: ")
    
        passenger_numbers = input_str.split(",")

        if validated_passenger_data(passenger_numbers):
            print("Numbers are valid")
            break

    return passenger_numbers


def validated_passenger_data(values):

    try:
        [int(value) for value in values]
        if len(values) != 4:
            raise ValueError(
                f"Exactly 4 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False


    if passenger_numbers[0] in range(0, 999): 
        pass
    else: raise ValueError(
            f"A number between 0-999 required, you provided {passenger_numbers[0]}"
            )
    

    if passenger_numbers[1] in range(0, 60): 
        pass
    else: raise ValueError(
            f"A number between 0-60 required, you provided {passenger_numbers[1]}"
            )
     

    if passenger_numbers[2] in range(0, 250): 
        pass
    else: raise ValueError(
            f"A number between 0-250 required, you provided {passenger_numbers[2]}"
            )
     

    if passenger_numbers[3] in range(0, 13): 
        pass
    else: raise ValueError(
            f"A number between 0-13 required, you provided {passenger_numbers[3]}"
            )
     

    return True


get_passenger_numbers_data()


