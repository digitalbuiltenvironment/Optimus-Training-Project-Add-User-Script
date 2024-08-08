import os
import json
from excel_to_json import excel_to_json
from get_token import get_token
from elevate_token import elevate_token
from send_request import send_request

# Read Excel input, prepare JSON payloads
try:
    excel_to_json()
except:
    os._exit(1)

# Print out access to be granted for each user, for verification
cont_input = input("Proceed with request (y/n)? ")
if cont_input.lower() != "y":       # If not y, terminate early
    print("Stopped")
    os._exit(0)
print()

# Get access token
try:
    access_token = get_token()
except Exception as err:
    print("get_token responded with error: " + str(err))
    os._exit(1)
print()

# Elevate token permissions
try:
    access_token = elevate_token()
except Exception as err:
    print("\nelevate_token responded with error: " + str(err))
    os._exit(1)
print()

# Send JSON payloads sequentially
with open("json_requests.json", "r") as file:
    data = json.load(file)
for payload in data:
    print(payload["user"]["userName"])
    response = send_request(payload)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.json()["error"]["message"])
    print()

print("Completed")
