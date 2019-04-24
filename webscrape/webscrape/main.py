from utils import utils
from classes import Scraper

def change_settings():
    """Allows the user to change the application settings"""
    settings_data = utils.read_json("config/settings.json")
    settings_message = "Please Enter Number Corresponding To Desired Setting"
    # lists choices for the user to change the settings
    settings_choice = utils.check_input(
        settings_message, utils.SETTINGS_CHOICES)

    if settings_choice == utils.SETTINGS_CHOICES[0]:
        search_message = "Please Enter Number Of Seconds To Timeout For"
        search_time = utils.check_input(search_message)
        settings_data["searchPause"] = search_time

    elif settings_choice == utils.SETTINGS_CHOICES[1]:
        ua_message = "Please Enter String Of User Agent"
        user_agent = utils.check_input(ua_message)
        settings_data["userAgent"] = user_agent

    # writes new settings data to the file
    utils.write_json("config/settings.json", settings_data)

def query_google():
    """Starts the queruing process for the programme"""
    flag = utils.check_times()
    if flag != False:
        # Get User Agent
        user_agent = utils.read_json("config/settings.json")["userAgent"]
        # Prompt User To Enter Desired Query
        desired_query = input("What Do You Want To Query?: ")
        # Prompt User For Number Of Search Results
        message = "How Many Results Would You Like To Scrape"
        results_amount = utils.check_input(message)

        result_handler = Scraper(desired_query, results_amount, user_agent)

        result_handler.scrape()
        data_results = result_handler.return_data_points()

        save_message = "Please Choose Desired Saving Option"
        save_outcome = utils.check_input(save_message, utils.SAVE_CHOICES)

        if save_outcome == utils.SAVE_CHOICES[0]:
            utils.csv_or_excel(desired_query, data_results, "Excel")
        elif save_outcome == utils.SAVE_CHOICES[1]:
            utils.csv_or_excel(desired_query, data_results, "Csv")
        else:
            print(data_results)
    else:
        print(
            "Scraper Cooldown Has Not Been Changed, Please Wait To Use It Again")

if __name__ == '__main__':
    utils.check_working_folder()
    utils.check_directories()

    while True:
        choice_message = "Please Enter Number Corresponding To Desired Option"
        # lists choices that should be shown to the user
        menu_outcome = utils.check_input(choice_message, utils.PROGRAMME_CHOICES)

        # picks a choice based on what the user choice
        if menu_outcome == utils.PROGRAMME_CHOICES[0]:
            query_google()
        elif menu_outcome == utils.PROGRAMME_CHOICES[1]:
            change_settings()

        # check if user wants to exit
        exit_message = "Would You Like To Exit"
        exit_outcome = utils.check_input(exit_message, utils.CHOICES)
        if exit_outcome == "Yes":
            break

    print("End of Programme\n")
