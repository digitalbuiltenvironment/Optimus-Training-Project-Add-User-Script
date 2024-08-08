import pandas as pd
import json

def excel_to_json():
    xls = pd.ExcelFile("new_users_list.xlsx")

    # Read new users list into dataframe
    df_users = pd.read_excel(xls, sheet_name="new-users-list")
    df_users.columns = ["email", "first_name", "last_name", "role"]

    # Read template for roles code into dataframe
    template_code = pd.read_excel(xls, sheet_name="template-code")
    template_code.columns = ["discipline", "designation", "projects", "roles"]

    # Read template for API values mapping into dataframe
    api_mapping = pd.read_excel(xls, sheet_name="map-api-values").dropna(subset=["Code"])
    api_mapping["Code"] = api_mapping["Code"].astype("Int64")
    api_mapping["Combined"] = api_mapping.apply(lambda row: row["Org"] + ": " + row["Form"] if pd.notna(row["Org"]) else row["Form"], axis=1)
    mapping_dict = dict(zip(api_mapping["Code"], api_mapping["Combined"]))

    # Convert to dictionary format
    json_requests = df_users.to_dict(orient="records")

    # Loop through, populate JSON payload for each new user
    formatted_requests = []
    for record in json_requests:
        rec_firstname = record["first_name"]
        rec_lastname = record["last_name"]
        rec_email = record["email"]
        rec_info = template_code[template_code["designation"] == record["role"]]
        if rec_info.empty:      # Check for invalid role
            print("Error: \"" + str(record["role"]) + "\" role not defined")
            raise ValueError
        try:
            rec_projects = [int(num) for num in str(rec_info["projects"].item()).split(", ")]
        except ValueError:
            print("\nError: invalid input in \"" + record["role"] + "\" Projects tab")
            raise
        try:
            rec_roles = [int(num) for num in str(rec_info["roles"].item()).split(", ")]
        except ValueError:
            print("\nError: invalid input in \"" + record["role"] + "\" Roles tab")
            raise

        json_request = {
            "user": {
                "id": None,
                "name": rec_firstname,
                "surname": rec_lastname,
                "userName": rec_email,
                "emailAddress": rec_email,
                "phoneNumber": None,
                "jobTitle": None,
                "companyName": None,
                "officeLocation": None,
                "password": None,
                "isActive": True,
                "shouldChangePasswordOnNextLogin": True,
                "isTwoFactorEnabled": False,
                "isLockoutEnabled": True,
                "isEmailConfirmed": False,
                "externalAuthenticationProviderId": 1
            },
            "sendActivationEmail": True,
            "sendDirectoryInvitation": True,
            "setRandomPassword": True,
            "assignedRoles": rec_roles,
            "organizationUnits": rec_projects,
            "tags": []
        }
        formatted_requests.append(json_request)

        # Print for verification, check for valid mapping values
        print(rec_firstname + " " + rec_lastname + " "*4 + rec_email + " "*4 + record["role"])
        print("Projects tab:")
        for code in rec_projects:
            try:
                print(mapping_dict[code])
            except KeyError:
                print("\nError: " + str(code) + " not in Projects mapping values")
                raise
        print("Roles tab:")
        for code in rec_roles:
            try:
                print(mapping_dict[code])
            except KeyError:
                print("\nError: " + str(code) + " not in Roles mapping values")
                raise
        print()

    # Write JSON payloads into file
    with open("json_requests.json", "w") as json_file:
        json.dump(formatted_requests, json_file, indent=4)


# For testing purposes
if __name__ == "__main__":
    excel_to_json()
