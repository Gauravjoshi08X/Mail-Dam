from flask import request
from encryption import Encryptor
import databaseConnect
class mailUA_IP():
    def __init__(self):
        self.traces = {}
        self.values = list(self.traces.values())
        self.encryptor: Encryptor=Encryptor()

    def getUserAgent_IP(self) -> None:
        try:
            # gets data and encrypts
            list(map(lambda x: self.traces.update({x: self.encryptor.encryptCrutial(request.headers.__getitem__(x))}),
                    ["Sec-Ch-Ua-Platform", "Sec-Ch-Ua", "X-Real-Ip"]))
        except KeyError as e:
            return e
    
    def sendToDB(self) -> None:
        databaseConnect.insertData(device=self.values[0], UA=self.values[1])
