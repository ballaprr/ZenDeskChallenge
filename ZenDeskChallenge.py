import requests
# requests.exceptions import ConnectionError
import json
import pandas as pd
import random
import os
from dotenv import load_dotenv

load_dotenv()
def terminate():
    print("Thank you for using the viewer. Goodbye")
    exit()

# API request
res = requests.get("https://zcczendeskcodingchallenge4590.zendesk.com/api/v2/requests.json", auth = (os.environ.get('user'), os.environ.get('pwd')))

# Check if API is available
if (res.ok == True):
    print(" ")
else:
    print("API Unavailable")
    terminate()
res.raise_for_status()

# Data into Dataframe
data = res.json()
df = pd.DataFrame.from_dict(data)
df_nested_list = pd.json_normalize(data, record_path= ['requests'])

# Prompt for a ticket number if user wants a particular ticket
def ticket_number():
    ticket_num = input("Enter ticket number: ")
    ticket_num = (int)(ticket_num)
    ticket_num = ticket_num + 1
    return ticket_num

# Random generator for test cases
def Rando():
    n = random.randint(-50, 150)
    return n

# WHen the user selects menu, this is the method
def menu(number, testcase, numbertest):
    print("menu number: " + str(number))
    # User selects 1, all tickets then print all the tickets from the API using pandas
    if (number == 1):
        for i in range (2, len(df_nested_list['id'].values)):
            print("Ticket with subject '" + df_nested_list.loc[(df_nested_list['id']) == i, 'subject'].values[0] + " opened by " + str(df_nested_list.loc[(df_nested_list['id']) == i, 'requester_id'].values[0]) + " on " + str(df_nested_list.loc[(df_nested_list['id']) == i, 'updated_at'].values[0]))
    # If the user selects 2, the user is prompted what ticket to be inputed
    elif (number == 2):
        if (testcase == 0):
            # Prompt for ticket
            ticket_num = ticket_number()
            # Error handling to see if the ticket entered is in the api
            while (ticket_num < (int) or len(df_nested_list['id'].values) > 101):
                print("Ticket number out of bounds")
                ticket_num = ticket_number()
            # Checing testcases
        elif (testcase == -2):
            try:
                ticket_num = (int)(numbertest)
                ticket_num = ticket_num + 1
            except ValueError:
                ticket_num = Rando()
            while (ticket_num < 2 or ticket_num > 101):
                print("Ticket number out of bounds")
                ticket_num = Rando()
        print("Ticket with subject '" + df_nested_list.loc[(df_nested_list['id']) == ticket_num, 'subject'].values[0] + " opened by " + str(df_nested_list.loc[(df_nested_list['id']) == ticket_num, 'requester_id'].values[0]) + " on " + str(df_nested_list.loc[(df_nested_list['id']) == ticket_num, 'updated_at'].values[0]))

# Prompt for user to enter all tickets, a ticket, or to quit
def prompt():
    number = ""
    while (number != "quit"):
        print("")
        print("       Select view options:")
        print("        * Press 1 to view all tickets")
        print("        * Press 2 to view a tickets")
        print("        * Type 'quit' to exit")
        number = input()
        testcase = 0 
        print("number: " + str(number))
        try:
            int(number)
            number = (int)(number)
            if (number < 1 or number > 2):
                print("Not a valid input")
            menu(number, 0, -2)
        except ValueError:
            if (number == "quit"):
                terminate()

# Function for testcase
def TestCase():
    menu(1, 0, 0) # Checks to print all tickets
    for i in range (0, 4):
        n = random.randint(-50, 150)
        print("Ticket number: " + str(n))
        menu(2, -2, n)
    print("Ticket number: a")
    menu(2, -2, 'a')
    print("Ticket number :adf")
    menu(2, -2, 'adf')
 
# Main function
def main():
    decision = input("Type 'menu' to view options or 'quit' to exit, or 'test case': ")
    if (decision == "menu"):
        prompt()
    elif (decision == "quit"):
        print("")
    elif (decision == "test case"):
        TestCase()
    else:
        main()

print("Welcome to the ticket viewer")
main()

