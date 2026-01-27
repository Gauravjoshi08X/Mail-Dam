from flask import Flask, request, redirect, Response
from MailBud.utils.encryption import Encryptor
import flask as fk
import datetime, os
import MailBud.utils.databaseConnect as dc

# Custom modules
from MailBud.utils.locateIP import trackIP

class TrackingServer:
    # Global Variables
    # mailFolder: str=maiLanding.mailLand()
    def __init__(self, tracker: str="static/trackingPixel.png"):
        self.app = Flask(__name__) 
        self.encryptor: Encryptor=Encryptor()
        self.tracker=tracker
        # Bind routes to instance methods
        self.app.add_url_rule('/static/<emailID>', view_func=self.sendTracker)
        self.app.add_url_rule('/click/<emailID>/redirect', view_func=self.trackClick)

    def _getTrackerURL(self)-> str:
        parent_dir=os.path.dirname(__file__).removesuffix(r"\MailBud")
        full_URL=os.path.join(parent_dir, self.tracker)
        return full_URL

    def _logEvents(self, emailID: str, destination: str="")->None:
        opened_time=datetime.datetime.now()
        dc.DatabaseInsert().insertOpenEventData(opened_time, emailID)
        if destination:
            city=trackIP()
            print(city)
            dc.DatabaseInsert().insertEventData(city, emailID)

    # With no link
    '''
    This doc is written for me to not wander to find main function.
    sendTracker
    '''

    # TODO:  Fix duplicate entry
    def sendTracker(self, emailID) -> Response:
        print(emailID)
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
    server.app.run(debug=True, port=5000)
