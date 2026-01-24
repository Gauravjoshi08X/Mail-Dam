from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  email import encoders
import base64, logging, json
# import connectFrontend

class MailTransmit():
	# Installed App Flow requires a sequence of strings to request during the flow
	SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

	def __init__(self, serverLink, g_cred):
		self.serverLink=serverLink
		self.g_cred=g_cred
		self.service=self._gmailAuthenticate()
		

	# don't know how it does but used by gmailAPI
	def _gmailAuthenticate(self):
		# refresh_token: str=connectFrontend.getName().get("refresh_token")
		with open(self.g_cred, 'r') as f:
			data = json.load(f)
			creds = Credentials(
			token=None,  # access token will be auto-fetched
			refresh_token="1//0gAyvIEgTbh14CgYIARAAGBASNwF-L9IrHXYiCDxMQHXZKy21alPMXk7IT7w5OnTNm8yUnmnR8YM45xLrOf3sYaVXgFrK9Bysmb8",
			client_id=data['web']['client_id'],
			client_secret=data['web']['client_secret'],
			token_uri="https://oauth2.googleapis.com/token",
			scopes=["https://www.googleapis.com/auth/gmail.send"]
		)
		return build("gmail", "v1", credentials=creds)

	# function to build html template for different version of link
	def _buildHTML(self, link: str|None, message_text: str, to: str) -> str:
		linkHTML=""
		if link:
			linkHTML=f"""<a href="{self.serverLink}/click/{to}/redirect?url={link}">{link}</a>"""
		# Embed tracking pixel
		htmlContent = f"""
			<html>
				<body>
				<p>{message_text}</p>
				<img src="{self.serverLink}/static/{to}" width="1" height="1"/>
				{linkHTML}
				</body>
			</html>
		"""
		return htmlContent

	def sendMessage(self, sender: str, to: str, subject: str, message_text: str, link: str=None, attachment=None):
		message=MIMEMultipart("mixed")
		message["to"] = to
		message["from"] = sender
		message["subject"] = subject

		alt=MIMEMultipart("alternative")
		alt.attach(MIMEText(self._buildHTML(link, message_text, to), "html"))
		message.attach(alt)

		if (attachment):
			file_data = base64.b64decode(attachment['data'])
			main_type, sub_type = attachment["mime_type"].split("/")
			part = MIMEBase(main_type, sub_type)
			part.set_payload(file_data)
			encoders.encode_base64(part)
			part.add_header(
				"Content-Disposition",
				f'attachment; filename="{attachment["filename"]}"')	
			message.attach(part)

		raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
		body = {"raw": raw_message}
		self.send_now = self.service.users().messages().send(userId="me", body=body).execute()
		return logging.debug(f"Message sent. ID: {self.send_now['id']}")