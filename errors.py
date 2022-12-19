def send_message(error_code):
   if error_code == 1:
      print("Ticker is invalid, please verify and enter again.")
   elif error_code == 2:
      print("Dates are invalid, please verify and enter again.")
   elif error_code == 3:
      print("The range requested exceeds the capabilities of this software, please enter a shorter date range.")
   elif error_code == 4:
      print("Upload failed becuse database could not be accessed. Please make sure the file exists and is not being used by other processes, then try again.")
