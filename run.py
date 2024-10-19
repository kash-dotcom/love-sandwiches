# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():

    while True:
        """
        Get Sales figures input from the user
        Run a while loop to collect a valid string of data from the user
        via the terminal, which must be a string of 6 numbers separated by 
        a commas. The loop will repeate data, until it is valid.
        """
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, spearted by commas")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ")
                
        sales_data = data_str.split(",")
        #split spring by commas and returns as a list 
        validate_data(sales_data)
    
        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string vlaues into intergers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values] #trying to convert each value into a interger
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales workesheet updated succesfully.\n")

def calucalate_surplus_data(sales_row):
    """
    Compare sales with stick and calucate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Postive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """

    print("Calcuating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock.pop(-1)

    pprint(stock_row)


def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calucalate_surplus_data(sales_data)


print("Welcome to Love Sandwiches Data Automation")

main()
