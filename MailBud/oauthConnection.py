from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from typing import Any
from flask import Flask, Response, request
class Oauth():
    # Installed App Flow requires a sequence of strings to request during the flow
    SCOPES = ['openid', 'email', 'profile', "https://www.googleapis.com/auth/gmail.send"]

    def __init__(self, g_cred, redirectURI):
        self.g_cred=g_cred
        self.session={}
        self.redirectURI=redirectURI
    
    app=Flask(__name__)

    @app.route("/auth/google", methods=["POST"])
    def generate_auth_url(self) -> Any:
        flow = Flow.from_client_secrets_file(
            self.g_cred,
            scopes=self.SCOPES,
            redirect_uri=self.redirectURI
        )
        
        auth_url, state = flow.authorization_url(
            access_type='offline',  # Gets refresh token
            include_granted_scopes='true'
        )
        
        # Store 'state' in session for security verification later
        self.session['state'] = state
        self.response={}
        self.response['auth_url']=auth_url
        return self.response
    

    @app.route("/auth/callback")
    def oauth_callback(self):
        state = self.session['state']
        
        flow = Flow.from_client_secrets_file(
            self.g_cred,
            scopes=self.SCOPES,
            state=state,
            redirect_uri=self.redirectURI
        )
        
        flow.fetch_token(authorization_response=request.url)
        
        # Now use credentials to build Gmail service or get user info
        self.credentials = flow.credentials
        print(self.credentials)

if __name__=="__main__":
    mail=Oauth(r"C:\Users\Gaurav\VSCode\Mail-Dam\src\certs\g_cred.json", "http://localhost:5000/oauth/callback")
    mail.app.run(debug=True)
