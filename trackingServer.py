from flask import Flask, request, redirect, Response
import flask as fk
app = Flask(__name__) 
# With no link
@app.route('/image/<emailID>')
def sendTracker(emailID) -> Response:
    with open("loginLog.log", "a") as logs:
        # to log from where the request is made 
        userAgent = request.headers.get('User-Agent', 'Unknown')
        logs.write(f"{emailID}|{userAgent}\n")
    return fk.send_file("image/trackingPixel.png", mimetype="image/png")

# with link
@app.route('/click/<emailID>/redirect')
def trackClick(emailID) -> Response:
    # Extract the destination URL from query parameters
    destination = request.args.get("url") # gets args redirect?url="example.com"
    with open("loginLog.log", "a") as logs:
        logs.write(f"{emailID}|{destination}\n")
    # Redirect user to their intended destination
    if (not destination.startswith(("http://www.", "https://www.", "https://", "http://"))):
        return redirect(f"https://www.{destination}")

if __name__ == '__main__':
    app.run(debug=True)