# We'll be using:
# - the Python DateTime strftime() method
# - APIs and making POST Requests
# - Authorization Headers
# - Environment Variables

import requests
from my_vars import *

APP_ID = nutritionix_APP_ID # this is defined in a separate 'my_vars.py' file, covered in .gitignore
API_KEY = nutritionix_API_KEY # this is defined in a separate 'my_vars.py' file, covered in .gitignore

age_input = int(input("What is your age?"))
weight_input = int(input("What is your weight (in kg) ?"))
height_input = int(input("And finally, what is your height (in cm) ?"))

nutritionix_query = input("What did you do today in your workout?")

nutritionix_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutritionix_PARAM = {
	"query" : nutritionix_query,
	"weight_kg" : weight_input,
	"height_cm" : height_input,
	"age" : age_input
}

HEADERS = {
	"x-app-id" : APP_ID,
	"x-app-key": API_KEY

}

response = requests.post(url=nutritionix_ENDPOINT, json=nutritionix_PARAM, headers=HEADERS)
result = response.json()
print(result) # for testing only

#now using a tool called Sheety at https://sheety.co/ we get our 'workout_tracker' google sheet populated
# with data from the input interpreted by nutritionix

# to check how to do this we use the sheety documentation: https://sheety.co/docs/requests