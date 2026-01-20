import csv
from mailTransmit import MailTransmit
import connectFrontend as cf;
def SEND():
    filename:str = input("Enter the CSV filename: ")
    mail=MailTransmit("https://9xkmd6fc-5000.inc1.devtunnels.ms", r"C:\Users\Gaurav\VSCode\Mail-Dam\src\certs\g_cred.json")
    try:
        textData: dict = cf.getData()
        imgAttach: dict = cf.getFile()
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                mail.sendMessage(sender=textData.get("sender"), 
                                to=row[0],
                                subject=textData.get("subject"),
                                message_text=textData.get("message"),
                                image_attachments=imgAttach)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__=="__main__":
    SEND()