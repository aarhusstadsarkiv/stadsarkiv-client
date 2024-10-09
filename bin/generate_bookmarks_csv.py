""""
Generate a new CSV file with bookmarks and emails.

Usage:

    python bin/generate_bookmarks_csv.py

This script will need two files:

    data/users.csv
    data/bookmarks.csv

From these files it generates the `bookmarks_with_emails.csv` file.
This file is the same as the `bookmarks.csv` file, but with an additional `email` field.

"""

import csv
import os

# get base path as the directory of the current file
# base_dir = os.path.dirname(os.path.abspath(__file__))

bookmarks_csv = os.path.join("data", "csv", "bookmarks.csv")
users_csv = os.path.join("data", "csv", "users.csv")
bookmarks_with_emails_csv = os.path.join("data", "csv", "bookmarks_with_emails.csv")


def read_resource_ids_by_email(file, email):
    resource_ids = []
    with open(file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"] == email:
                resource_ids.append(row["resource_id"])
    return resource_ids


def count_unique_emails(file):
    email_set = set()
    with open(file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            email_set.add(row["email"])
    return len(email_set)


def read_csv_to_dict(file, key_field):
    data_dict = {}
    with open(file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_dict[row[key_field]] = row
    return data_dict


def add_email_to_bookmarks(bookmarks_file, users_file, output_file):

    # Read users data into a dictionary with user_id as key
    users = read_csv_to_dict(users_file, "user_id")

    # Open the bookmarks file and prepare to read
    with open(bookmarks_file, "r") as file:
        reader = csv.DictReader(file)
        bookmarks = list(reader)

    # Define the fieldnames for the new CSV, adding 'email' field
    fieldnames = bookmarks[0].keys() | {"email"}

    # Create or open the new bookmarks file with email included
    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for bookmark in bookmarks:
            user_id = bookmark["user_id"]

            # Find the user's email from the users dictionary
            email = users.get(user_id, {}).get("email")
            if email is None:
                continue

            bookmark["email"] = email
            writer.writerow(bookmark)


# Add email to bookmarks and save to new CSV
print("Exporting bookmarks")
add_email_to_bookmarks(bookmarks_csv, users_csv, bookmarks_with_emails_csv)

# example usage. Find by email
bookmarks = read_resource_ids_by_email(bookmarks_with_emails_csv, "dennis.iversen@gmail.com")
print("Test to find bookmarks by email")
print(bookmarks)

print("Count unique emails:")
print(count_unique_emails(bookmarks_with_emails_csv))

# count all bookmarks
bookmarks_with_emails = sum(1 for row in csv.reader(open(bookmarks_with_emails_csv)))

print(f"Num bookmarks {bookmarks_with_emails}")
