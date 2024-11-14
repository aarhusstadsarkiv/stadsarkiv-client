#!/usr/bin/env python
"""
Extract email from the csv file and save it to a new file named data/csv/emails.csv
This csv files contains a single column with the header "email"
"""

import csv


csv_file = "data/csv/users.csv"


# read the csv file and extract email and save it to a new file named data/emails.csv
print("Extracting emails from the csv file")
with open(csv_file, "r") as f:
    reader = csv.DictReader(f)
    with open("data/csv/emails.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["email"])
        for row in reader:
            writer.writerow([row["email"]])

# get num rows in the csv file
num_rows = sum(1 for row in csv.reader(open("data/csv/users.csv")))
print(f"Extracted {num_rows} emails from the csv file")
