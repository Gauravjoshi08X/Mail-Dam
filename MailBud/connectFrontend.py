from flask import Flask, request, jsonify, json
from typing import Any
import base64
import mimetypes
import protoMain as pm
import databaseConnect as dc

app=Flask(__name__)

@app.route("/getdata", methods=["POST", "GET"])
def getData() -> dict[str, Any]:
    data = request.get_json()
    with open("sendData.json", "w") as fp:
        json.dump(data,fp)
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
    rt: str=dc.DatabaseFetch().fetchRTData(user);
    response={"isUser": dc.DatabaseFetch().isUser(user), "refresh_token": rt}
    return jsonify(response)

@app.route("/sendmail", methods=["GET"])
def sendMail():
    pm.SEND()
    return "Mail Sent Successfully!"

if __name__=="__main__":
    app.run(debug=True)
