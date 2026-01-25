from flask import Flask, request, json
from typing import Any
import base64, time, os
import mimetypes
from MailBud.utils import databaseConnect as dc
from MailBud.mailTransmit import MailTransmit
from MailBud.utils.iterEmails import iterEmail
import dotenv

dotenv.load_dotenv("src/certs/credential.env")

app=Flask(__name__)

class Config:
    def __init__(self):
        self.tunnel_url: str = os.getenv("TUNNEL")
        app.add_url_rule("/getdata", view_func=self.getData, methods=["POST", "GET"])
        app.add_url_rule("/sendfile", view_func=self.getFile, methods=["POST", "GET"])
        app.add_url_rule("/sendname", view_func=self.getName, methods=["POST"])
        app.add_url_rule("/sendmail", view_func=self.sendMail, methods=["GET"])
    
    def getData(self) -> dict[str, Any]:
        data = request.get_json()
        return data
    
    def getFile(self) -> dict[str, Any]:
        files = request.files.getlist('file')
        for file in files:
            if (file.filename.split(".")[1]!="csv"):
                file_content = file.read()

                # Encode to base64
                encoded_data = base64.b64encode(file_content).decode('utf-8')
                
                # Get MIME type
                mime_type, _ = mimetypes.guess_type(file.filename)
                if mime_type is None:
                    mime_type = 'application/octet-stream'  # Default for unknown types

                # Create attachment object
                attachment = {
                    'filename': file.filename,
                    'data': encoded_data,
                    'mime_type': mime_type
                }
                with open("attach.json", "w") as fp:
                    json.dump(attachment, fp)
                return attachment
            else:

                file.save("emails.csv")

    def getName(self) -> dict:
        data = request.get_json()
        user: str=data.get("name").strip()
        with open("MailBud/transit/user.txt", "w") as fp:
            fp.write(user)
        response={"isUser": dc.DatabaseFetch().isUser(user)}
        return response
    
    def sendMail(self):
        mailData=self.getData()
        print(mailData)
        with open("MailBud/transit/user.txt", "r") as fp:
            rt=dc.DatabaseFetch().fetchRTData(fp.read())
            mail=MailTransmit(self.tunnel_url, "src/certs/g_cred.json", rt)
            try:
                with open("MailBud/transit/sendData.json", "r") as mailData:
                    with open("MailBud/transit/attach.json", "r") as fileData:
                        sendData: dict=json.load(mailData)
                        fileAttach: dict=json.load(fileData)
                        for email in iterEmail():
                            mail.sendMessage(sender=dc.DatabaseFetch().fetchEmailData(fp.read()), to=email,
                                            subject=sendData.get("subject"),
                                            message_text=sendData.get("message"),
                                            link=sendData.get("link"), attachment=fileAttach)
                            dc.DatabaseInsert().insertEmailData(email, sendData.get("subject"), str(time.strftime("%Y:%m:%d %H:%M:%S")))
                        dc.DatabaseInsert().insertPRJData(sendData.get("project"))
            except Exception as e:
                print(f"Error: {e}")

        os.remove("MailBud/transit/sendData.json")
        os.remove("MailBud/transit/user.txt")
        return {"msg": "Mail Sent Successfully!"}
    
if __name__=="__main__":
    app.run(debug=True, port=5005)
