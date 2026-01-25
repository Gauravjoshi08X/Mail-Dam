from flask import Flask, request, redirect, Response
from MailBud.utils.encryption import Encryptor
import flask as fk, json
import time, os
import MailBud.utils.databaseConnect as dc

# Custom modules
from MailBud.utils.locateIP import trackIP
import MailBud.utils.maiLanding as maiLanding

class TrackingServer:
    # Global Variables
    # mailFolder: str=maiLanding.mailLand()
    def __init__(self, tracker: str=r"C:\Users\Gaurav\VSCode\Mail-Dam\src\static\trackingPixel.png"):
        self.app = Flask(__name__) 
        self.encryptor: Encryptor=Encryptor()
        self.tracker=tracker
        # Bind routes to instance methods
        self.app.add_url_rule('/static', view_func=self.sendTracker)
        self.app.add_url_rule('/click/redirect', view_func=self.trackClick)

    def _logEvents(self, destination: str="")->None:
        if (destination==""):
            opened_time=time.strftime("%Y-%m-%d-%I:%M:%S %p %Z")
            dc.DatabaseInsert().insertOpenEventData(opened_time)
        else:
            # with open("src/logs/traces.json") as fp:
                # location=json.load(fp).get("X-Real-City")
            dc.DatabaseInsert().insertEventData(location="Kathmandu")
    # With no link
    '''
    This doc is written for me to not wander to find main function.
    sendTracker
    '''

    def sendTracker(self) -> Response:
        self._logEvents()
        response=fk.send_file(self.tracker, mimetype="image/png")
        # kinda forcing agent to return these
        response.headers["Accept-CH"] = "Sec-CH-UA, Sec-CH-UA-Platform"
        # this restricts browser to cache tracker but may not work with gmail
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response
    
    # With Link
    def _trackClickHelper(self, destination: str)-> None:
        # trackIP()
        self._logEvents(destination)

    '''
    This doc is written for me to not wander to find main function.
    sendTracker
    '''
    def trackClick(self) -> Response:
        # Extract the destination URL from query parameters
        destination = request.args.get("url") # gets args redirect?url="example.com"
        self._trackClickHelper(destination)
        # Redirect user to their intended destination
        if (not destination.startswith(("http://www.", "https://www."))):
            return redirect(f"https://www.{destination}")

if __name__ == '__main__':
    server=TrackingServer()
    server.app.run(debug=True, port=5000)
