import requests
import json

def trackIP(path: str="src/logs/traces.json") -> None:
    try:
        with open(path, "r") as fp:
            AllData: dict = json.load(fp)
        ipData = AllData.get("X-Real-Ip")
        url = f"http://ip-api.com/json/{ipData}"
        city = requests.get(url).json().get("city")
        AllData["X-Real-City"]= city
        
        with open(path, "w") as fp:
            json.dump(AllData, fp, indent=2)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
            requests.exceptions.RequestException) as e:
        print(f"Exception: {e}")

if __name__=="__main__":
    trackIP()