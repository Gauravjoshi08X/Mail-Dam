from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def gmail_authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("gCred.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

def send_message(service, sender, to, subject, message_text):
    message=MIMEMultipart("alternative")
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject


    # Embed tracking pixel
    html_content = f"""
    <html>
      <body>
        <p>{message_text}</p>
        <img src="https://9xkmd6fc-5000.inc1.devtunnels.ms/image/{to}" width="1" height="1"/>
      </body>
    </html>
    """

    message.attach(MIMEText(html_content, "html"))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw_message}

    send_message = service.users().messages().send(userId="me", body=body).execute()
    print(f"Message sent. ID: {send_message['id']}")

if __name__ == "__main__":
    service = gmail_authenticate()
    send_message(service, "gauravjoshi3140@gmail.com", "joshigaurav9011@gmail.com", "Hello from Maildam", "This is a test email.")