import email
from flask import Flask, Response, request, json, jsonify
from typing import Any
import base64, os, datetime
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
        self.tunnel_url: str = os.getenv("MAIL_TUNNEL")
        self.app.add_url_rule("/sendmail", view_func=self.sendMail, methods=["POST", "GET"])
        self.app.add_url_rule("/sendname", view_func=self.getName, methods=["POST"])
        self.app.add_url_rule("/getname", view_func=self.getName, methods=["POST"])
  
    def getName(self) -> dict:
        data = request.get_json()
        rawUser=data.strip().split(" ")
        user=" ".join([rawUser[0].capitalize(), rawUser[1].capitalize()])
        response={"isUser": dc().isUser(user)}
        return response

    def sendMail(self) -> dict[str, Any]:
        project = request.form.get("project")
        subject = request.form.get("subject")
        message = request.form.get("message")
        link = request.form.get("link")
        name = request.form.get("name").strip().split(" ")
        formatted_name=" ".join([name[0].capitalize(), name[1].capitalize()])
        files = request.files.getlist('file')
        attachment = {}
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
            else:
                rt=dc().fetchRTData(formatted_name)
                sendr=dc().fetchEmailData(formatted_name)
                mail=MailTransmit(self.tunnel_url, "src/certs/g_cred.json", rt)
                content = file.read().decode("utf-8")
                emails=iterEmail(content)
                if (attachment=={}):
                    for email in emails:
                        di().insertPRJData(project, formatted_name)
                        mail.sendMessage(sendr, email, subject, message, link)
                        di().insertEmailData(email, formatted_name, datetime.datetime.now())
                else:
                    for email in emails:
                        di().insertPRJData(project, formatted_name)
                        mail.sendMessage(sendr, email, subject, message, link, attachment)
                        di().insertEmailData(email, formatted_name, datetime.datetime.now())

        return jsonify({"msg": "Emails Sent Successfully!"})

if __name__=="__main__":
    instance=Config()
    instance.app.run(debug=True, port=5005)
