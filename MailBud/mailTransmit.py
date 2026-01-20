from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  email import encoders
import base64, logging


class MailTransmit():
	# Installed App Flow requires a sequence of strings to request during the flow
	SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

	def __init__(self, serverLink, g_cred):
		self.serverLink=serverLink
		self.g_cred=g_cred
		self.service=self._gmailAuthenticate()
		

	# don't know how it does but used by gmailAPI
	def _gmailAuthenticate(self):
		flow = InstalledAppFlow.from_client_secrets_file(self.g_cred, self.SCOPES)
		creds = flow.run_local_server(port=0)
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

	def sendMessage(self, sender: str, to: str, subject: str, message_text: str, link: str=None, attachment: dict={}):
		message=MIMEMultipart("alternative")
		message["to"] = to
		message["from"] = sender
		message["subject"] = subject

		message.attach(MIMEText(self._buildHTML(link, message_text, to), "html"))
		file_data = base64.b64decode(attachment['data'])
		if (len(attachment.keys())!=0):
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(file_data)
			encoders.encode_base64(part)
			raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
			part.add_header('Content-Disposition', f"attachment; filename= {attachment['filename']}")
			message.attach(part)

		body = {"raw": raw_message}
		self.send_now = self.service.users().messages().send(userId="me", body=body).execute()
		return logging.debug(f"Message sent. ID: {self.send_now['id']}")