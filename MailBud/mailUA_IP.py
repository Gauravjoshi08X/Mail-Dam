from flask import request, json
from encryption import Encryptor

def getUserAgent_IP() -> None:
    with open("src/logs/traces.json", "w") as fp:
        traces = {}
        encryptor: Encryptor=Encryptor()
        try:
            list(map(lambda x: traces.update({x: encryptor.encryptCrutial(request.headers.__getitem__(x))}),
                    ["Sec-Ch-Ua-Platform", "Sec-Ch-Ua", "X-Real-Ip"]))
            json.dump(traces, fp, indent=2)
        except KeyError as e:
            return e

if __name__=="__main__":
    getUserAgent_IP()
