from flask import Flask, request, redirect, Response
import flask as fk
import time, os

# Custom modules
from mailUA_IP import getUserAgent_IP
from locateIP import trackIP
import maiLanding

# Global Variables
# mailFolder: str=maiLanding.mailLand()

app = Flask(__name__) 

# With no link
@app.route('/static/<emailID>')
def sendTracker(emailID) -> Response:
    openedTime=time.strftime("%Y-%m-%d-%I:%M:%S %p %Z")
    with open("src/logs/loginLog.log", "a") as logs:
        logs.write(f"{emailID}|{openedTime}\n")
    # trackIP()
    parentDir=os.path.dirname(__file__).removesuffix(r"\MailBud")
    tracker="src/static/trackingPixel.png"
    response=fk.send_file(os.path.join(parentDir, tracker), mimetype="image/png")
    response.headers["Accept-CH"] = "Sec-CH-UA, Sec-CH-UA-Platform"
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    # this restricts browser to cache tracker but may not work with gmail
    return response

# with link
@app.route('/click/<emailID>/redirect')
def trackClick(emailID) -> Response:
    # Extract the destination URL from query parameters
    openedTime=time.strftime("%Y-%m-%d-%I:%M:%S %p %Z")
    destination = request.args.get("url") # gets args redirect?url="example.com"
    with open("src/logs/loginLog.log", "a") as logs:
        logs.write(f"{emailID}|{openedTime}|{destination}\n")
    getUserAgent_IP()
    trackIP()
    # Redirect user to their intended destination
    if (not destination.startswith(("http://www.", "https://www."))):
        return redirect(f"https://www.{destination}")

if __name__ == '__main__':
    app.run(debug=True)
