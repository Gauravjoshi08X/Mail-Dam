import imaplib, dotenv, os

dotenv.load_dotenv("src/certs/credential.env")
class MailLand():
	def __init__(self, target):
		self.user: str = os.getenv("GOOGLE_ACCOUNT_USER_NAME")
		self.password: str = os.getenv("GOOGLE_ACCOUNT_APP_PASSWORD")
		self.host = 'imap.gmail.com'
		self.targetSpam: str = target

	def mailLand(self)-> str:

		# Connect securely with SSL
		with imaplib.IMAP4_SSL(self.host) as mail:
			try:
				# Login and select Spam folder
				mail.login(self.user, self.password)
				# select gmail folders like Inbox, Spam
				mail.select('[Gmail]/Spam')

				status, email = mail.search(None, f'(SUBJECT "{self.targetSpam}")')
				# email_id returns binary index of email if found else ''
				if (email!=[b'']):
					return f"Email with subject '{self.targetSpam}' found in the folder."
				else:
					return f"Email with subject '{self.targetSpam}' not found in the folder."
			except Exception as e:
				return f"Exception: {e}"

if __name__=="__main__":
	instance=MailLand(target="charged your ZBD account")
	folder: str=instance.mailLand()
	print(folder)