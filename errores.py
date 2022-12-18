def error_handling(error_code):
   if len(ticker_data) == 0:
    error_code == 1
    print("Ticker is invalid, please verify and enter again.")
   elif start >= end or end > datetime.now():
    error_code = 2
    print("Dates are invalid, please verify and enter again.")
   elif period > max_years:
    error_code = 3
    print("The range requested exceeds the capabilities of this software, please enter a shorter date range.")