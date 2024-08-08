import requests
from dotenv import load_dotenv, set_key
import os

def elevate_token():
    load_dotenv(override=True)

    # Base url currently points to QAS platform, can be changed
    base_url = "https://optimus-qas.fulcrumhq.build"
    endpoint = "/api/TokenAuth/Scope/Elevate"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Authorization": f"Bearer {os.getenv("ACCESS_TOKEN")}"
    }

    response = requests.post(base_url+endpoint, headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.json()["error"]["message"])
    
    print("Elevate Token successful")
    elevate_token = response.json()["result"]["accessToken"]
    set_key(".env", "ELEVATE_TOKEN", elevate_token)
    return elevate_token


# For testing purposes
if __name__ == "__main__":
    elevate_token()
