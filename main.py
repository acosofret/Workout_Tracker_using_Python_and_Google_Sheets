# We'll be using:
# - the Python DateTime strftime() method
# - APIs and making POST Requests
# - Authorization Headers
# - Environment Variables

import requests
from my_vars import *
from datetime import datetime

# First, we create a workout_tracker spreadsheet in a free Google Sheets account
# The sheet has the following columns: Date	/ Time	/ Exercise	/ Duration	/ Calories

# Then, we use the nutritionix endpoint to interpret and return workout
# data based on raw text input (similar to chatGPT):
# nutritionix documentation: https://docx.syndigo.com/developers/docs/nutritionix-api-guide

APP_ID = nutritionix_APP_ID # this is defined in a separate 'my_vars.py' file, covered in .gitignore
API_KEY = nutritionix_API_KEY # this is defined in a separate 'my_vars.py' file, covered in .gitignore

age_input = int(input("What is your age?")) # optional parameter
weight_input = int(input("What is your weight (in kg) ?")) # optional parameter
height_input = int(input("And finally, what is your height (in cm) ?")) # optional parameter

nutritionix_query = input("What did you do today in your workout?") # required parameter

nutritionix_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutritionix_PARAM = {
	"query" : nutritionix_query,
	#"weight_kg" : weight_input,
	#"height_cm" : height_input,
	#"age" : age_input
}
# we use headers for authentication, so our sensible data is not shown in the browser (as parameters)
HEADERS = {
	"x-app-id" : APP_ID,
	"x-app-key": API_KEY,
}

response = requests.post(url=nutritionix_ENDPOINT, json=nutritionix_PARAM, headers=HEADERS)
result = response.json()
print(result)
# from result we'll only need the data in our spreadsheet columns: Date	/ Time	/ Exercise	/ Duration	/ Calories
# we get date & time using datetime module:
entry_date = datetime.now().strftime("%d/%m/%Y")
entry_time = datetime.now().strftime("%X")

#now using a tool called Sheety at https://sheety.co/ we get our 'workout_tracker' google sheet populated
# with data from the input interpreted by nutritionix
# to check how to do this we use the sheety documentation: https://sheety.co/docs/requests

sheety_ENDPOINT = my_sheety_ENDPOINT

# we pull out the exercise name, duration and calories from the nutritionix response
# and add everything in a dict:
for exercise in result["exercises"]:
	workout_sheet_inputs = {
		"workout" : {
			"date" : entry_date,
			"time" : entry_time,
			"exercise" : exercise["name"].title(),
			"duration" : exercise["duration_min"],
			"calories" : exercise["nf_calories"]
		}
	}

	bearer_headers = {
		"Authorization": f"Bearer {my_nutritionix_bearer_token}"  # this is to enhance security
	}

	sheet_row_filling = requests.post(sheety_ENDPOINT, json=workout_sheet_inputs, headers=bearer_headers)

	print(sheet_row_filling.text)

### *** BUG: The duration input in the duration column is inputed wrong (probablu the column needs formatting to suit data type)
