import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('menu_requirements')

def input_or_check_meals():
    """
    Allows the user to choose if they want to input new flight data for meals or print flight meal data for kitchen
    """
    print("Welcome to Legion Internationals flight meal ordering service.\n")
    while True:
        choice = input("Would you like to input flight meals or check flight meals?\n").lower()
        if choice == "flight meals":
            if confirm_choice(f"You selected {choice}. "):
                get_passenger_numbers_data()
                break
        elif choice == "check flight meals":
            if confirm_choice(f"You selected {choice}. "):
                show_required_meals()
                break
        else:
            print("Incorrect selection. Please try again")


def confirm_choice(choice):
    """
    confirms users choice
    """
    while True:
        confirm = input(f"{choice}Is that correct? y/n\n").lower()
        if confirm == "y":
            return True
        elif confirm == "n":
            return False
        else:
            print("Incorrect selection. Please try again")


def get_passenger_numbers_data():
    """
    Get passenger numbers from User
    """
    while True:
        print("Please enter flight number and number of passengers")
        print("Enter flight number bis class passenger and crew numbers, seperated by commas.")
        print("Example: 300,50,140,10\n")

        input_str = input("Enter your data here:\n")
    
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
    data[0] = f"LI{data[0]}"
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
    Divides bis class numbers by 6 dishes offered to bis class passengers
    """
    return round(passenger_data[1] / 6)

def update_bisclass_worksheet(passenger_data, bisclass_meals):
    """
    Updates Business class meal numbers in work sheet adding new row
    """
    print("Updating meal numbers...\n")
    data = [passenger_data[0], bisclass_meals, bisclass_meals, bisclass_meals, bisclass_meals, bisclass_meals, bisclass_meals]
    bisclass_meals_worksheet = SHEET.worksheet("bis")
    bisclass_meals_worksheet.append_row(data)
    print("Passenger meals updated sucessfully.\n")   



def special_request(passenger_data):
    """
    Allows user to input special requests for bis class passengers
    """
    while True:
        print("Any special requests required?")
        answer = input("y/n:\n")
        if answer == "y":
            pass
        elif answer == "n":
            return
        else:
            print("Please enter y or n.") 
        print("Enter Special requests as required below.\n")
        while True:
            print("Select seat number between 1 - 60.")
            seat = input("Seat Number:\n")
            try:
                seat = int(seat)
                if seat in range(0, 61):
                    break
            except ValueError:
                pass

            print(f"A number between 0-60 required, you provided {seat}")

        print("Enter special request")
        special = input("Special Request:\n")

        update_special_request(passenger_data, seat, special)


def update_special_request(passenger_data, seat, special_request):
    """
    updates
    """
    print("Updating special request's...\n")
    data = [passenger_data[0], seat, special_request]
    special_request_worksheet = SHEET.worksheet("special")
    special_request_worksheet.append_row(data)
    print("Special request's updated sucessfully.\n")

def show_required_meals():
    """
    retrieves meal data for specific flight using flight number for kitchen to prepare.
    """
    print("Please enter flight number.")
    print("Example: LI300")
    flight_num = input("Flight number:\n")

    passengers_worksheet = SHEET.worksheet("passengers")
    bis_worksheet = SHEET.worksheet("bis")
    economycrew_worksheet = SHEET.worksheet("economycrew")
    special_worksheet = SHEET.worksheet("special")

    cells = passengers_worksheet.findall(flight_num)
    bis_cells = bis_worksheet.findall(flight_num)
    economycrew_cells = economycrew_worksheet.findall(flight_num)
    special_cells = special_worksheet.findall(flight_num)

    h1 = ["Flight Number", "Bis", "Economy", "Crew"]
    h2 = ["Flight Number", "Chicken", "Beef"]
    h3 = ["Flight Number", "Chicken", "Beef", "Lamb", "Pork", "fish", "Vegetarian"]
    h4 = ["Flight Number", "Seat", "Special Request"]

    print(tabulate([passengers_worksheet.row_values(cell.row) for cell in cells], headers=h1))
    print(tabulate([bis_worksheet.row_values(cell.row) for cell in bis_cells], headers=h3))
    print(tabulate([economycrew_worksheet.row_values(cell.row) for cell in economycrew_cells], headers=h2))
    print(tabulate([special_worksheet.row_values(cell.row) for cell in special_cells], headers=h4))


def get_and_store_flight_details():
    data = get_passenger_numbers_data()
    passenger_data = [int(num) for num in data]
    update_passenger_worksheet(passenger_data)
    economy_meals = economy_crew_meals(passenger_data)
    update_economycrew_worksheet(passenger_data, economy_meals)
    bisclass_meals = bis_class_meals(passenger_data)
    update_bisclass_worksheet(passenger_data, bisclass_meals)
    special_request(passenger_data)


MENU_OPTIONS = """
Welcome to Legion International's meal ordering terminal

Please choose from one of the following options:
    1) Enter meal orders
    2) Print meal orders
    3) Exit terminal
>>>
"""

def main():
    keep_running = True
    while keep_running:
        choice = input(MENU_OPTIONS)

        if choice == "1":
            get_and_store_flight_details()
        elif choice == "2":
            show_required_meals()
        elif choice == "3":
            keep_running = False
        else:
            print("Incorrect option.. Please try again...")


if __name__ == "__main__":
    main()