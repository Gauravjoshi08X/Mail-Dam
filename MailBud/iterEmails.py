import csv, os
def iterEmail() -> list:
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "emails.csv")
    emails=[]
    with open(csv_path) as fp:
        item=csv.reader(fp)
        row=list(map(lambda x: x.lower(),item.__next__()))
        if ("email" in row or "emails" in row):
            try:
                if "email" in row:
                    index = row.index("email")
                elif "emails" in row:
                    index = row.index("emails")
                for i in item:
                    if (i[index]!=''):
                        emails.append(i[index])
                return emails
            except Exception as e:
                print(e)

if __name__=="__main__":
    iterEmail()