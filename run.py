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


def validated_passenger_data(passenger_numbers):
    """
    Validates the data input from user, gives error message if incorrect.
    """

    try:
        passenger_numbers = [int(value) for value in passenger_numbers]
        if len(passenger_numbers) != 4:
            raise ValueError(
                f"Exactly 4 values required, you provided {len(passenger_numbers)}"
            )

        if passenger_numbers[0] in range(0, 1000):
            pass
        else: 
            raise ValueError(
                f"A number between 0-999 required, you provided {passenger_numbers[0]}"
                )
            

        if passenger_numbers[1] in range(0, 61): 
            pass
        else: 
            raise ValueError(
                f"A number between 0-60 required, you provided {passenger_numbers[1]}"
                )
        

        if passenger_numbers[2] in range(0, 251): 
            pass
        else: 
            raise ValueError(
                f"A number between 0-250 required, you provided {passenger_numbers[2]}"
                )
        

        if passenger_numbers[3] in range(0, 14): 
            pass
        else: 
            raise ValueError(
                f"A number between 0-13 required, you provided {passenger_numbers[3]}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
     

    return True


def update_passenger_worksheet(data):
    """
    Updates passenger numbers in work sheet, adding a new row
    """
    print("Updating Passenger numbers...\n")
    passenger_worksheet = SHEET.worksheet("passengers")
    # Prefix flight number with `LI`.
    data[0] = f"LI{data[0]}"
    # flight_number, biz, economy, crew = data
    # flight_number = f"LI{flight_number}"
    passenger_worksheet.append_row(data)
    print("Passenger numbers updated sucessfully.\n")

def economy_crew_meals(passenger_data):
    """
    collects flight number, adds economy passengers and crew together 
    adds 20 divides total by two. 
    """
    return round((passenger_data[2] + passenger_data[3] + 20) / 2)

    

def update_economycrew_worksheet(passenger_data, economy_meals):
    """
    Updates economycrew meal numbers in work sheet adding new row
    """
    print("Updating meal numbers...\n")
    data = [passenger_data[0], economy_meals, economy_meals]
    economycrew_worksheet = SHEET.worksheet("economycrew")
    economycrew_worksheet.append_row(data)
    print("Passenger meals updated sucessfully.\n")

def bis_class_meals(passenger_data):
    """
    collects flight number, adds economy passengers and crew together 
    adds 20 divides total by two. 
    """
    return round(passenger_data[1] / 6)

def update_bisclass_worksheet(passenger_data, economy_meals):
    """
    Updates economycrew meal numbers in work sheet adding new row
    """
    print("Updating meal numbers...\n")
    data = [passenger_data[0], bisclass_meals, bisclass_meals, bisclass_meals, bisclass_meals, bisclass_meals, bisclass_meals]
    economycrew_worksheet = SHEET.worksheet("bis")
    economycrew_worksheet.append_row(data)
    print("Passenger meals updated sucessfully.\n")

data = get_passenger_numbers_data()
passenger_data = [int(num) for num in data]
update_passenger_worksheet(passenger_data)
economy_meals = economy_crew_meals(passenger_data)
update_economycrew_worksheet(passenger_data, economy_meals)
bisclass_meals = bis_class_meals(passenger_data)
update_bisclass_worksheet(passenger_data, bisclass_meals)



