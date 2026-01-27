import csv, io

def iterEmail(csv_data: str) -> list:
    emails = []
    try:
        reader = csv.reader(io.StringIO(csv_data))
        header = [x.lower() for x in next(reader)]
        if "email" in header:
            index = header.index("email")
        elif "emails" in header:
            index = header.index("emails")
        else:
            return emails

        for row in reader:
            value = row[index].strip()
            if value:
                emails.append(value)
    except Exception as e:
        print("Error parsing CSV:", e)
    return emails