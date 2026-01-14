import csv
from mailTransmit import MailTransmit
filename:str = input("Enter the CSV filename: ")
subject: str = input("Enter Subject: ")
message: str = input("Enter Message: ")
link: str|None = input("Enter Link (if there): ")
mail=MailTransmit("https://9xkmd6fc-5000.inc1.devtunnels.ms", r"C:\Users\Gaurav\VSCode\Mail-Dam\src\certs\g_cred.json")
try:
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            mail.sendMessage("prototype5039@gmail.com", row[0], subject, message, link)

except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
except Exception as e:
    
    print(f"Error: {e}")
