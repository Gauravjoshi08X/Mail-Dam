import json, os
from mailTransmit import MailTransmit
from iterEmails import iterEmail
def SEND():
    mail=MailTransmit("https://9xkmd6fc-5000.inc1.devtunnels.ms", r"C:\Users\Gaurav\VSCode\Mail-Dam\src\certs\g_cred.json")
    try:
        send_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sendData.json")
        mailData = open(send_data, "r")
        sendData: dict=json.load(mailData)
        attach_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "attach.json")
        imgData = open(attach_path, "r")
        imgAttach: dict=json.load(imgData)
        for email in iterEmail():
            mail.sendMessage(sender=sendData.get("sender"), 
                            to=email,
                            subject=sendData.get("subject"),
                            message_text=sendData.get("message"),
                            link=sendData.get("link"),
                            attachment=imgAttach)
        imgData.close()
        mailData.close()
    except FileNotFoundError:
        print(f"Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__=="__main__":
    SEND()