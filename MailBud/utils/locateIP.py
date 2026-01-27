import requests
import json
from flask import request
def trackIP() -> str:
    try:
        ip_data=request.headers.__getitem__("X-Real-Ip")
        url = f"http://ip-api.com/json/{ip_data}"
        city = requests.get(url).json().get("city")
        return city
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
            requests.exceptions.RequestException) as e:
        print(f"Exception: {e}")

if __name__=="__main__":
    trackIP()