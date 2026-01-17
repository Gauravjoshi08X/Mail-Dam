from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
import requests
import os
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.send"
]

CLIENT_SECRETS = r"C:\Users\Gaurav\VSCode\Mail-Dam\src\certs\g_cred.json"
REDIRECT_URI = "https://9xkmd6fc-5000.inc1.devtunnels.ms/oauth/callback"

@app.route("/auth/google")
def auth_google():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )

    return redirect(auth_url)

@app.route("/oauth/callback")
def oauth_callback():
    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )

        # Make sure request.url has ?code=...
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials

        # Get user info
        userinfo = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {creds.token}"}
        ).json()

        # Now write to file only if everything succeeded
        path = os.path.join(BASE_DIR, "data.txt")
        with open(path, "w") as f:
            f.write(f"{userinfo['email']} {userinfo['name']} {creds.refresh_token}")

        print("File written successfully")
        return "OAuth completed, file saved!"

    except Exception as e:
        print("Error in OAuth callback:", e)
        return f"OAuth failed: {e}", 500

if __name__=="__main__":
    app.run(debug=True)