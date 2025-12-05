import imaplib, dotenv, os

def mailLand()-> str:
	dotenv.load_dotenv("src/certs/credential.env")

	user: str = os.getenv("GOOGLE_ACCOUNT_USER_NAME")
	password: str = os.getenv("GOOGLE_ACCOUNT_APP_PASSWORD")

	host = 'imap.gmail.com'
	targetSpam = ""

	# Connect securely with SSL
	with imaplib.IMAP4_SSL(host) as mail:

		# Login and select Spam folder
		mail.login(user, password)
		# select gmail folders like Inbox, Spam
		mail.select('[Gmail]/Spam')

		status, email = mail.search(None, f'(SUBJECT "{targetSpam}")')
		# email_id returns 1 if found else ''
		if email:
			return f"Email with subject '{targetSpam}' found in the folder."
		else:
			return f"Email with subject '{targetSpam}' not found in the folder."

if __name__=="__main__":
	print(mailLand())