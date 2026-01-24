from flask import Flask, request, jsonify, json
from typing import Any
import base64
import mimetypes
from MailBud.utils import databaseConnect as dc
from MailBud.mailTransmit import MailTransmit
from MailBud.utils.iterEmails import iterEmail
app=Flask(__name__)

@app.route("/getdata", methods=["POST", "GET"])
def getData() -> dict[str, Any]:
    data = request.get_json()
    return data

@app.route("/sendfile", methods=["POST", "GET"])
def getFile() -> dict[str, Any]:
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

@app.route("/sendname", methods=["POST"])
def getName() -> dict:
    data = request.get_json()
    user: str=data.get("name").strip()
    with open("MailBud/transit/user.txt", "w") as fp:
        fp.write(user)
    response={"isUser": dc.DatabaseFetch().isUser(user)}
    return response

@app.route("/sendmail", methods=["GET"])
def sendMail():
    with open("MailBud/transit/user.txt", "r") as fp:
        rt=dc.DatabaseFetch().fetchRTData(fp.read())
        mail=MailTransmit("https://9xkmd6fc-5010.inc1.devtunnels.ms", "src/certs/g_cred.json", rt)
    # try:
    with open("MailBud/transit/sendData.json", "r") as mailData:
        with open("MailBud/transit/attach.json", "r") as fileData:
            sendData: dict=json.load(mailData)
            fileAttach: dict=json.load(fileData)
            for email in iterEmail():
                mail.sendMessage(sender=sendData.get("sender"), to=email,
                                subject=sendData.get("subject"),
                                message_text=sendData.get("message"),
                                link=sendData.get("link"), attachment=fileAttach)
    # except Exception as e:
    #     print(f"Error: {e}")
    return {"msg": "Mail Sent Successfully!"}
    
if __name__=="__main__":
    app.run(debug=True, port=5005)
