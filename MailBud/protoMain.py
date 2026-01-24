from MailBud.mailTransmit import MailTransmit
from MailBud.utils.iterEmails import iterEmail
import json
def SEND():
    mail=MailTransmit("https://9xkmd6fc-5010.inc1.devtunnels.ms", "src/certs/g_cred.json")
    try:
        with open("MailBud/transit/sendData.json", "r") as mailData:
            with open("MailBud/transit/attach.json", "r") as fileData:
                sendData: dict=json.load(mailData)
                fileAttach: dict=json.load(fileData)
                for email in iterEmail():
                    mail.sendMessage(sender=sendData.get("sender"), to=email,
                                    subject=sendData.get("subject"),
                                    message_text=sendData.get("message"),
                                    link=sendData.get("link"), attachment=fileAttach)

    except Exception as e:
        print(f"Error: {e}")