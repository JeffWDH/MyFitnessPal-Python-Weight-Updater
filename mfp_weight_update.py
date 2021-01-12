import requests
import datetime
import json
from bs4 import BeautifulSoup

mfp_username = "Username"
mfp_password = "Password"

# Based on:
# https://www.reddit.com/r/Myfitnesspal/comments/g77vj5/bashbased_netcode_for_changing_goals_and/

def update_mfp_weight(username:str, password:str, weight:float):
  # Create session to maintain cookies
  session = requests.Session()

  # Grab login page
  mfpLoginPage = session.get("https://www.myfitnesspal.com/account/login")

  # Scrape authenticity_token
  parse = BeautifulSoup(mfpLoginPage.content, "html.parser")
  authenticity_token = parse.find('input', attrs={'name': 'authenticity_token'})['value']

  # Login form POST data
  post = {
      'username': username,
      'password': password,
      'authenticity_token': authenticity_token
  }

  # Submit login
  session.post("https://www.myfitnesspal.com/account/login", data=post)

  # Refresh API and grab data
  apijson = session.get("https://www.myfitnesspal.com/user/auth_token?refresh=true")
  apidata = json.loads(apijson.text)

  # HTTP Headers
  headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': "Bearer " + apidata['access_token'],
    'mfp-user-id': apidata['user_id'],
    'mfp-client-id': 'mfp-main-js',
    'Origin': 'https://www.myfitnesspal.com'
  }

  # Array to be turned into JSON
  json_data = {
    "items": [{
      "type": "weight",
      "value": weight,
      "unit": "pounds",
      "date": datetime.datetime.now().strftime("%F")
    }]
  }

  # Turn array into JSON string
  post = json.dumps(json_data)

  # Submit data
  response = session.post("https://api.myfitnesspal.com/v2/measurements", data=post, headers=headers)

  if response.status_code == 200:
    return "OK"
  else:
    return "Fail"

# Test request
result = update_mfp_weight(mfp_username, mfp_password, 220)
print(result)