from flask import Flask, request, redirect, Response
import flask as fk
import time
app = Flask(__name__) 
# With no link
@app.route('/image/<emailID>')
def sendTracker(emailID) -> Response:
    openedTime=time.strftime("%Y-%m-%d-%I:%M:%S %p %Z")
    with open("loginLog.log", "a") as logs:
        logs.write(f"{emailID}|{openedTime}\n")
    return fk.send_file("src/image/trackingPixel.png", mimetype="image/png")

# with link
@app.route('/click/<emailID>/redirect')
def trackClick(emailID) -> Response:
    # Extract the destination URL from query parameters
    openedTime=time.strftime("%Y-%m-%d-%I:%M:%S %p %Z")
    destination = request.args.get("url") # gets args redirect?url="example.com"
    with open("loginLog.log", "a") as logs:
        logs.write(f"{emailID}|{openedTime}|{destination}\n")
    # Redirect user to their intended destination
    if (not destination.startswith(("http://www.", "https://www.", "https://", "http://"))):
        return redirect(f"https://www.{destination}")

if __name__ == '__main__':
    app.run(debug=True)
