import requests
import json
from flask import request
def trackIP(path: str="src/logs/traces.json") -> None:
    try:
        all_data={}
        ip_data=request.headers.__getitem__("X-Real-Ip")
        print(f"IP Address: {ip_data}")
        url = f"http://ip-api.com/json/{ip_data}"
        city = requests.get(url).json().get("city")
        all_data["X-Real-City"]= city
        
        with open(path, "w") as fp:
            json.dump(all_data, fp, indent=2)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
            requests.exceptions.RequestException) as e:
        print(f"Exception: {e}")

if __name__=="__main__":
    trackIP()