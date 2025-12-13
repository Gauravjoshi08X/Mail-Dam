from flask import Flask, request, redirect, Response
import flask as fk
import time, os

# Custom modules
from mailUA_IP import getUserAgent_IP
from locateIP import trackIP
import maiLanding

class TrackingServer:
    # Global Variables
    # mailFolder: str=maiLanding.mailLand()
    def __init__(self, tracker: str="src/static/trackingPixel.png", log:str="src/logs/loginLog.log"):
        self.app = Flask(__name__) 
        self.tracker=tracker
        self.logs=log
        # Bind routes to instance methods
        self.app.add_url_rule('/static/<emailID>', view_func=self.sendTracker)
        self.app.add_url_rule('/click/<emailID>/redirect', view_func=self.trackClick)

    def _getTrackerURL(self)-> str:
        parent_dir=os.path.dirname(__file__).removesuffix(r"\MailBud")
        full_URL=os.path.join(parent_dir, self.tracker)
        return full_URL

    def _logEvents(self, emailID: str, destination: str=None)->None:
        opened_time=time.strftime("%Y-%m-%d-%I:%M:%S %p %Z")
        log_info=f"{emailID}|{opened_time}\n"
        if destination:
            log_info=f"{emailID}|{opened_time}|{destination}\n"
        with open(self.logs, "a") as fp:
            fp.write(log_info)

    # With no link
    '''
    This doc is written for me to not wander to find main function.
    sendTracker
    '''
    def sendTracker(self, emailID) -> Response:
        self._logEvents(emailID)
        response=fk.send_file(self._getTrackerURL(), mimetype="image/png")
        # kinda forcing agent to return these
        response.headers["Accept-CH"] = "Sec-CH-UA, Sec-CH-UA-Platform"
        # this restricts browser to cache tracker but may not work with gmail
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"

        return response

    # With Link
    def _trackClickHelper(self, emailID:str, destination: str)-> None:
        self._logEvents(emailID, destination)
        getUserAgent_IP()
        trackIP()
    
    '''
    This doc is written for me to not wander to find main function.
    sendTracker
    '''
    def trackClick(self, emailID: str) -> Response:
        # Extract the destination URL from query parameters
        destination = request.args.get("url") # gets args redirect?url="example.com"
        self._trackClickHelper(emailID, destination)
        # Redirect user to their intended destination
        if (not destination.startswith(("http://www.", "https://www."))):
            return redirect(f"https://www.{destination}")

if __name__ == '__main__':
    server=TrackingServer()
    server.app.run(debug=True)
