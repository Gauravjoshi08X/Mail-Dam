from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
import requests
import os, uuid, redis
from MailBud.utils.databaseConnect import DatabaseInsert

class OauthConnection:
    def __init__(self):
        self.app = Flask(__name__)

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.tunnel_url: str = os.getenv("AUTH_TUNNEL")
        self.REDIS_URL=os.getenv("REDIS_URL")
        self.SCOPES = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/gmail.send"
        ]
        self.CLIENT_SECRETS = r"src/certs/g_cred.json"
        self.REDIRECT_URI = f"{self.tunnel_url}/oauth/callback"
        self.session_id=""

        self.app.add_url_rule('/auth/google', view_func=self.auth_google)
        self.app.add_url_rule('/oauth/callback', view_func=self.oauth_callback)
        self.app.add_url_rule('/oauth/getsession', view_func=self.getSession)

    def auth_google(self):
        self.flow = Flow.from_client_secrets_file(
            self.CLIENT_SECRETS,
            scopes=self.SCOPES,
            redirect_uri=self.REDIRECT_URI
        )
        
        auth_url, _ = self.flow.authorization_url(
            access_type="offline",
            prompt="consent"
        )

        return redirect(auth_url)

    def oauth_callback(self):
        try:
            flow = Flow.from_client_secrets_file(
                self.CLIENT_SECRETS,
                scopes=self.SCOPES,
                redirect_uri=self.REDIRECT_URI
            )
            
            flow.fetch_token(authorization_response=request.url)
            creds = flow.credentials
            
            userinfo = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {creds.token}"}
            ).json()
            
            DatabaseInsert().insertUserData(self.sessionRedis()[1], userinfo['email'], userinfo['name'], creds.refresh_token)
            
            return "OAuth completed"
        
        except Exception as e:
            print("Error in OAuth callback:", e)
            return f"OAuth failed: {e}", 500
    
    def sessionRedis(self):      
            session_id=""
            for _ in range(8):
                session_id+=str(uuid.uuid4())
            session_id=session_id.replace('-', "")

    def sessionRedis(self):
            for _ in range(8):
                self.session_id+=str(uuid.uuid4())
            self.session_id=self.session_id.replace('-', "")

            user_id=int(str(int(uuid.uuid4()))[:10])
            res=redis.from_url(self.REDIS_URL)
            res.set(name=self.session_id, value=user_id, ex=7*24*60*60)
            return (self.session_id, user_id)
    # Only runs ater sessionRedis is called. using async is better.
    def getSession(self)->str:
        return self.session_id
            
if __name__ == "__main__":
    oauth_conn = OauthConnection()
    oauth_conn.app.run(port=5000)
