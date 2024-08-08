# Optimus Training Project - Add User Script
Python script that uses APIs to automatically add new users to Optimus Training Project in O2 QAS and gives access to folders using rules from Excel input
## Project Setup
In the project base directory, create a .env file and input the service account credentials:
```
SVC_USERNAME='<svc_username>'
SVC_PASSWORD='<svc_password>'
```
Create Python virtual environment in the base directory:
```
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate.bat  # cmd
# or
source .venv/bin/activate   # bash

# Install requirements
pip install -r requirements.txt
```
## Set up Excel input
To add templates for new roles, edit the `template-code` sheet
- Enter the discipline and designation (role)
- Referring to `map-api-values`, find the codes of the folders to be given access, and input under `O2 Projects tab` and `O2 Roles tab` respectively
	- Ensure codes are comma separated, e.g. `25, 28, 253`

To add new users, edit the `new-users-list` sheet
- Enter the Email, first name, last name and role respectively
	- Ensure the role matches one of the designations in `template-code` sheet

The `map-api-values` sheet won’t need to be modified
- Unless mapping codes change, or new folders are to be added
- Use Chrome Developer tools to examine the form creation request and obtain new codes, or communicate with LeapThought

## Running the Script
Run `python main.py`

The script will process the Excel file, generate the JSON payload for each new user and print out the folders they will be given access to, for verification purposes

There will be a prompt to continue
- if there are issues in the printout, type “n” to stop the program, and rectify the Excel
- if there are no problems, type “y” to continue

The program will use the SVC account credentials to obtain and get permissions for the auth token
- if there are any errors to the API, it will be printed in the terminal and the program will stop

The program will use the auth token to request to add each user in 
“new-users-list” sequentially
- if there are no errors, it will print “200 Success”
- if the user already exists in the system, it will print 
“500 username is already taken.”

## Modifications to work with O2 Prod
**(untested as of 07/08/24)**
To make the script work for other projects in O2 Production, go into “get_token.py”, “elevate_token.py” and “send_request.py” and change the base_url to 
“https://optimus.fulcrumhq.build”

Organisation Unit code may need to be edited to match the new project

`map-api-values` sheet may need to be updated with codes for each individual project
