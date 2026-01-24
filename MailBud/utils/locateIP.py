import requests
import json
from MailBud.utils.encryption import Encryptor

def trackIP(path: str="src/logs/traces.json") -> None:
    encryptor: Encryptor=Encryptor()
    try:
        with open(path, "r") as fp:
            all_data: dict = json.load(fp)
        # ip_data is encrypted by mailUA_IP module
        ip_data = encryptor.decryptCrutial(all_data.get("X-Real-Ip"))
        url = f"http://ip-api.com/json/{ip_data}"
        city = requests.get(url).json().get("city")
        all_data["X-Real-City"]= encryptor.encryptCrutial(city)
        
        with open(path, "w") as fp:
            json.dump(all_data, fp, indent=2)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
            requests.exceptions.RequestException) as e:
        print(f"Exception: {e}")

if __name__=="__main__":
    trackIP()