from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64, logging


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# logs to display console errors
logging.basicConfig(
    level=logging.ERROR,
    format='%(levelname)s - %(message)s'
)

# don't know how it does but used by gmailAPI
def gmail_authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("gCred.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)


def send_message(service, sender, to, subject, messageText):
	message=MIMEMultipart("alternative")
	message["to"] = to
	message["from"] = sender
	message["subject"] = subject

    # Embed tracking pixel
	htmlContent = """
		<html>
			<body>
			<p>{Message}</p>
			<img src="https://9xkmd6fc-5000.inc1.devtunnels.ms/image/{To}" width="1" height="1"/>
			{Link}
			</body>
		</html>
	"""
	
	# Add links (optional)
	option=input("Do you want to send a link? (y/n)\n").lower()
	if (option == "y"):
		link = input("Enter the URL:\n").strip()
		# url to capture traffic and redirection
		htmlContent=htmlContent.format(Message=messageText, To=to, Link=f'<a href="https://9xkmd6fc-5000.inc1.devtunnels.ms/click/{to}/redirect?url={link}">{link}</a>')

	elif (option=="n"):
		htmlContent=htmlContent.format(Message=messageText, To=to, Link='')

	else:
		# logs error. can be done using print but I will be using for debugging in future so been using it.
		logging.error("Enter valid input.")

	message.attach(MIMEText(htmlContent, "html"))

	raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
	body = {"raw": raw_message}

	send_message = service.users().messages().send(userId="me", body=body).execute()
	print(f"Message sent. ID: {send_message['id']}")

if __name__ == "__main__":
	service = gmail_authenticate()
	send_message(service, "gauravjoshi3140@gmail.com", "joshigaurav9011@gmail.com", "Hello from Maildam", "This is a test email.")