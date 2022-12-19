from datetime import datetime
from datetime import timedelta

import errors as errors
import database_functions as db


exit_command = False

while not exit_command:
    user_command = input("Choose between 'get', 'check', and 'display' a ticker\n").lower()

    if user_command == 'get':
        ticker = input("Enter ticker: ").upper()
        st_date = input("Enter start date (YYYY-MM-DD): ")
        fn_date = input("Enter final date (YYYY-MM-DD): ")

        get_error_code = db.get_ticker_data(ticker, st_date, fn_date)
        errors.send_message(get_error_code)

    elif user_command == 'check':
        ticker = input("Enter ticker: ").upper()
        ticker_meta_data = db.check_ticker_data(ticker)

        if ticker_meta_data is None:
            print("No data has been gathered for that ticker yet.")
        else:
            print("Start date: " + ticker_meta_data["start_date"])
            print("End date: " + ticker_meta_data["end_date"])

    elif user_command == 'display':
        ticker = input("Enter ticker: ").upper()
        ticker_meta_data = db.check_ticker_data(ticker)

        if ticker_meta_data is None:
            print("No data has been gathered for that ticker yet.")
        else:
            display_error_code = db.plot_ticker(ticker)
            errors.send_message(display_error_code)

    elif user_command == 'exit':
        exit_command = True

    else:
        print("Not a valid command.")

print("Thank you for using our services, have a great day.")
