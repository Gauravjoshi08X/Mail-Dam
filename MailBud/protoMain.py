import csv, json
from mailTransmit import MailTransmit
from iterEmails import iterEmail
def SEND():
    # filename:str = input("Enter the CSV filename: ")
    mail=MailTransmit("https://9xkmd6fc-5000.inc1.devtunnels.ms", r"C:\Users\Gaurav\VSCode\Mail-Dam\src\certs\g_cred.json")
    try:
        mailData = open("sendData.json", "r")
        sendData: dict=json.load(mailData)

        imgData = open("attach.json", "r")
        imgAttach: dict=json.load(imgData)
        for email in iterEmail():
            mail.sendMessage(sender=sendData.get("sender"), 
                            to=email,
                            subject=sendData.get("subject"),
                            message_text=sendData.get("message"),
                            link=sendData.get("link"),
                            attachment=imgAttach)
    except FileNotFoundError:
        print(f"Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__=="__main__":
    SEND()