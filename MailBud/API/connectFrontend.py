from flask import Flask, request, json, session
from typing import Any
import base64, os, time
import mimetypes
from MailBud.utils.databaseConnect import DatabaseFetch as dc
from MailBud.utils.databaseConnect import DatabaseInsert as di
from MailBud.mailTransmit import MailTransmit
from MailBud.utils.iterEmails import iterEmail
import dotenv

dotenv.load_dotenv("src/certs/credential.env")


class Config:
    def __init__(self):
        self.app=Flask(__name__)
        self.app.secret_key=os.getenv("FLASK_SECRET_KEY")
        self.tunnel_url: str = os.getenv("TUNNEL")
        self.app.add_url_rule("/sendfile", view_func=self.getFile, methods=["POST", "GET"])
        self.app.add_url_rule("/sendname", view_func=self.getName, methods=["POST"])
        self.app.add_url_rule("/getname", view_func=self.getName, methods=["POST"])
        self.app.add_url_rule("/sendmail", view_func=self.sendMail, methods=["POST", "GET"])
  
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
                with open("MailBud/transit/attach.json", "w") as fp:
                    json.dump(attachment, fp)
                return attachment
            else:

                file.save("MailBud/transit/emails.csv")

    def getName(self) -> dict:
        data = request.get_json()
        rawUser=data.get("name").strip().split(" ")
        user=" ".join([rawUser[0].capitalize(), rawUser[1].capitalize()])
        response={"isUser": dc().isUser(user)}
        return response
    
    def sendMail(self):
        mailData=request.get_json()
        rawUser=mailData.get("name").strip().split(" ")
        user=" ".join([rawUser[0].capitalize(), rawUser[1].capitalize()])
        rt=dc().fetchRTData(user)
        sendr=dc().fetchEmailData(user)
        mail=MailTransmit(self.tunnel_url, "src/certs/g_cred.json", rt)
        try:
            di().insertPRJData(mailData.get("project"), user)
            with open("MailBud/transit/attach.json", "r") as fileData:
                fileAttach: dict=json.load(fileData)
                for email in iterEmail():
                    mail.sendMessage(sender=sendr, to=email, subject=mailData.get("subject"),message_text=mailData.get("message"),link=mailData.get("link"), attachment=fileAttach)
                    di().insertEmailData(email, mailData.get("subject"), str(time.strftime("%Y:%m:%d %H:%M:%S")))
        except Exception as e:
            print(f"Error: {e}")
        return {"msg": "Mail Sent Successfully!"}
    
if __name__=="__main__":
    instance=Config()
    instance.app.run(debug=True, port=5005)
