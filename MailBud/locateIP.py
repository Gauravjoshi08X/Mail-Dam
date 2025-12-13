import requests
import json

def trackIP(path: str="src/logs/traces.json") -> None:
    try:
        with open(path, "r") as fp:
            all_data: dict = json.load(fp)
        ip_data = all_data.get("X-Real-Ip")
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