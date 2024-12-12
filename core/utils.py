import requests


def get_current_location():
    response = requests.get("http://ip-api.com/json/")

    if response.status_code == 200:
        data = response.json()
    else:
        data = None
    return data
