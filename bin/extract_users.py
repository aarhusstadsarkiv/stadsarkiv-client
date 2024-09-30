import csv


csv_file = "data/users.csv"

# read the csv file and extract email and save it to a new file named data/emails.csv
with open(csv_file, "r") as f:
    reader = csv.DictReader(f)
    with open("data/emails.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["email"])
        for row in reader:
            writer.writerow([row["email"]])
