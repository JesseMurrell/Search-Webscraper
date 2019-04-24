import os
import sys
import json
import pathlib
import datetime
import subprocess
import pandas as pd

# Programme Constants
PROGRAMME_CHOICES = [
    "Query Google",
    "Change Settings"
]
SETTINGS_CHOICES = [
    "Search Timeout: The Time Between Google Queries",
    "User Agent: Add A User Agent String To The Programme (Optional)"
]
CHOICES  = [
    "Yes",
    "No"
]
SAVE_CHOICES = [
    "Save Data To Excel File",
    "Save Data To Csv File",
    "Don't Save Data (Outputs To Terminal)"
]
# Programme Paths

SETTINGS_PATH = str(pathlib.Path("config/settings.json"))
LIGHTHOUSE_PATH  = str(pathlib.Path("config/lighthouse.json"))
CONFIG_FOLDER = str(pathlib.Path("config/"))
DATA_FOLDER = str(pathlib.Path("data/"))

# Programme Utility Functions
# --- Json Functions

def read_json(path):
    """Reads a json file into python dictionary

    Parameters:
        path: the path to the json file
    Returns:
        python dictionary object containing file contents
    """
    with open(path, "r") as json_file:
        return load_json(json_file.read())

def load_json(string):
    """Loads json from string data

    Parameters:
        string: string to add to convert to json object
    """
    return json.loads(string)

def write_json(path, data):
    """Writes python dictionary data to json file

    Parameters:
        path: path to the json file
        data: python dictionary to be saved to the file
    """
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)

# File Functions

def check_working_folder():
    if os.path.basename(os.getcwd()) != "Webscrape":
        raise Exception("Please Run Programme From It's Base Directory")

def check_directories():
    """Checks if file(s) exists at programme initialisation"""
    # checks that all paths are present in folder
    if os.path.isdir(CONFIG_FOLDER) == False:
        os.mkdir(CONFIG_FOLDER)
    if os.path.isdir(DATA_FOLDER) == False:
        os.mkdir(DATA_FOLDER)

    # checks if the settings file exists
    if os.path.isfile(SETTINGS_PATH) == False:
        # default settings file data
        settings_data = {
            "searchPause": 1,
            "currentDate": None,
            "userAgent": None
            }
        write_json(SETTINGS_PATH, settings_data)

    # checks if the lighthouse settings file exists
    if os.path.isfile(LIGHTHOUSE_PATH) == False:
        # default lighthouse settings data
        lighthouse_data = {
            "extends": "lighthouse:default",
            "settings": {
                "onlyCategories": [
                    "performance"
                ]
            }
        }
        write_json(LIGHTHOUSE_PATH, lighthouse_data)


def joinPath(path1, path2):
    """ Joins two file paths

    Parameters:
        path1: 1st path
        path2: 2nd path
    Returns:
        a joined path object
    """
    return os.path.join(path1, path2)

# Datetime Functions

def get_current_time():
    """Gets the current time upon call (local time)

    Returns:
        datetime object of current time of function call
    """
    return datetime.datetime.now()

def get_time_delta(time1, time2):
    """Gets the time delta between two dates in seconds

    Parameters:
        time1: datetime object
        time2: datetime object
    Returns:
        float value of the number of seconds that have elapsed

    """
    time_difference = time1 - time2
    # gets the absolute value of the time delta (> 0)
    difference_in_seconds = abs(time_difference.total_seconds())
    return difference_in_seconds

def date_obj(date):
    """Create datetime object from date string

    Parameters:
        date: string object of desired date
    Returns:
        datatime representation of date
    """
    formatter = "%Y-%m-%d %H:%M:%S.%f"
    return datetime.datetime.strptime(date, formatter)

# String Functions

def querify_string(string):
    """Creates a queryable string for the google search engine

    Parameters:
        string: string to be querified
    Returns:
        querable string
    """
    return string.strip().replace(" ", "+")

def validate_string(string):
    """ Will validate a string for chars that will cause File Name Errors

    Parameters:
        string: any string to be validated
    Returns:
        string containing none of the invalid markers in them.
    """
    invalid_markers = ["\\", "/", ":", "\"", "|", "?", "*"]
    for markers in invalid_markers:
        string.replace(markers, "")
    return string

def get_link_info(element):
    """Extracts link data from href element while retaining protocol

    Parameters:
        element: string html element to be extracted
    Returns:
        extracted link element
    Example:
        element = /url?q=http://www.andersonpaak.com/&sa=U&ved=0ahUKEwirqbH98-PhAhXzSBUIHdaXAhgQFggoMAM&usg=AOvVaw3Cy9kHwjxnHssR3_8kmnbR
        omit_and = /url?q=http://www.andersonpaak.com/
        omit_from_equals = http://www.andersonpaak.com/
    """
    omit_and = element.split("&")[0]
    omit_from_equals = omit_and.split("=")[-1]
    return omit_from_equals

# User Input Functions

def list_options(iterable):
    """Enumerates an iterable and list the numbered contents

    Parameters:
        iterable: any iterable object (list, tuple, dict etc)
    """
    for i, item in enumerate(iterable):
        print("{}. {}".format(i+1, item))

def check_input(message, iterable = None):
    """Provides checks for integer values as well as list choices

    Parameters:
        message: message to be shown as the prompt for the choice
        iterable (None): a iterable object to choose an index from
    Returns:
        will return a string or a integer depending on what is given for
        the iterable parameter.
    """
    while True:
        # if iterable is not its default value
        if iterable != None:
            list_options(iterable)
        try:
            number = int(input("{}: ".format(message)))
        # exception if they enter nothing or a not number
        except (ValueError, UnboundLocalError):
            print("Please Enter A Valid Integer")
        else:
            # if iterable was given check that chosen number is within range
            if iterable != None:
                if number < 1 or number > len(iterable):
                    print("Please enter a valid number in range")
                else:
                    break
            else:
                break
    # returns an index of a string if a list was given or just a number
    return iterable[number - 1] if iterable != None else number

# Other Functions

def check_times():
    """Compares the time of the last programme start to the currrent"""
    # reads settings file and get the current date from it
    json_data = read_json("config/settings.json")
    date = json_data["currentDate"]
    # if the date is null in json and None in python
    if date == None:
        current_date = get_current_time()
        json_data["currentDate"] = str(current_date)
        write_json("config/settings.json", json_data)
        outcome = True
    else:
        # gets the current date
        current_date = get_current_time()
        # calculates the time delta in seconds between previous and current
        time_delta = get_time_delta(
            current_date, date_obj(json_data["currentDate"])
        )
        # if delta is less time than the definied pause
        if time_delta < json_data["searchPause"]:
            outcome = False
        # else write the new current date to the json file and proceed
        else:
            json_data["currentDate"] = str(current_date)
            write_json("config/settings.json", json_data)
            outcome = True

    return outcome

def call_cli_command(command_call):
    """Will run a command line call inside the python file

    Parameters:
        command_call: string of the command you would like to call
    Returns:
        bytes result of the command line call
    """
    # calls the command in shell
    call = subprocess.run(command_call, shell = True, capture_output=True)
    # returns the result in bytes as well as the sucess code (0 is success)
    return call.stdout, call.returncode

def get_encoding():
    """Gets the terminal encoding"""
    return sys.stdout.encoding

def csv_or_excel(query_name, data, identifier):
    """ Writes google results to excel or csv format

    Parameters:
        query_name: Queried string
        data: results parsed from data
        identifier: string that tells the functions what file format to save
    """
    query_name = validate_string("{}".format(query_name))
    date = str(get_current_time()).replace(":", ",").replace("-", ",")
    data_frame = pd.DataFrame(data)

    if identifier == "Excel":
        file_name = "{} - {}.xlsx".format(query_name, date)
        file_path = joinPath(DATA_FOLDER, file_name)

        data_to_excel = pd.ExcelWriter(file_path, engine="xlsxwriter")
        data_frame.to_excel(data_to_excel, sheet_name="Google Results")
        data_to_excel.save()

    elif identifier == "Csv":
        file_name = "{} - {}.csv".format(query_name, date)
        file_path = joinPath(DATA_FOLDER, file_name)
        data_frame.to_csv(file_path)

    print ("File {} Save to data directory".format(file_name))
