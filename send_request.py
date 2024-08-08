import requests
from dotenv import load_dotenv
import os
import json

def send_request(payload):
    load_dotenv(override=True)

    # Base url currently points to QAS platform, can be changed
    base_url = "https://optimus-qas.fulcrumhq.build"
    endpoint_create = "/api/services/app/User/CreateUser"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Accept": "text/plain",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv("ELEVATE_TOKEN")}",
        "Lt-Ou": "25"
    }

    response = requests.post(base_url+endpoint_create, headers=headers, json=payload)
    print(response.status_code)

    return response


# For testing purposes
if __name__ == "__main__":
    with open("json_requests.json", "r") as f:
        data = json.load(f)
    payload = data[-1]
    response = send_request(payload)
    print(response.content)
