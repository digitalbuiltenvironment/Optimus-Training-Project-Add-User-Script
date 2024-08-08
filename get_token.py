import requests
from dotenv import load_dotenv, set_key
import os

def get_token():
    load_dotenv(override=True)

    # Base url currently points to QAS platform, can be changed
    base_url = "https://optimus-qas.fulcrumhq.build"
    endpoint_auth = "/api/TokenAuth/Authenticate"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    payload = {
        "userNameOrEmailAddress": os.getenv("SVC_USERNAME"),
        "password": os.getenv("SVC_PASSWORD"),
        "rememberClient": False,
        "twoFactorRememberClientToken": None,
        "singleSignIn": False,
        "returnUrl": None
    }

    response = requests.post(base_url+endpoint_auth, headers=headers, json=payload)
    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.json()["error"]["message"])
    
    print("Get accessToken successful")
    access_token = response.json()["result"]["accessToken"]
    set_key(".env", "ACCESS_TOKEN", access_token)
    return access_token
        
    # response = requests.post(base_url+endpoint_auth, headers=headers, json=payload)
    # if response.status_code == 200:
    #     access_token = response.json()["result"]["accessToken"]
    #     set_key(".env", "ACCESS_TOKEN", access_token)
    #     # print(access_token)
    #     return(access_token)
    # else:
    #     print("Unable to get response with Code: ", response.status_code)
    # return -1


# For testing purposes
if __name__ == "__main__":
    get_token()
