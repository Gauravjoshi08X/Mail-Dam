from flask import Flask, request, json
from typing import Any
import base64
import mimetypes
app=Flask(__name__)
@app.route("/getdata", methods=["POST", "GET"])
def getData():
    data = json.dumps(request.get_json())
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
            return attachment

if __name__=="__main__":
    app.run(debug=True)
