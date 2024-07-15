import random
import os
import pandas as pd
import datetime as dt
from email.message import EmailMessage
import smtplib

# information of sender and receiver
my_email = "techypradhicksan@gmail.com"
pass_word = "wequphuzjwpobkqk"

# creating a list of files in a folder
path = "letter_templates"
all_files_list = os.listdir(path)
txt_files_list = [file for file in all_files_list if file.endswith(".txt")]

# finding today's date, month
time_class = dt.datetime
time_now = time_class.now()
date_today = time_now.day
month_today = time_now.month

# creating a dictionary out of people whose birthday is today
# dictionary syntax {name:[e_email, date, month]}
ppl_to_be_emailed = {}
with open("birthdays.csv") as birthday_data_file:
    bd_df = pd.read_csv(birthday_data_file)
    for (index, row) in bd_df.iterrows():
        date = row["day"]
        month = row["month"]
        if date == date_today and month == month_today:
            ppl_to_be_emailed[row["name"]] = [row["email"], date, month]

# sending mail for people in the list
dict_len = len(ppl_to_be_emailed)
if dict_len == 0:
    print("No one's birthday is today!")
else:
    for name in ppl_to_be_emailed:
        # picking out a random message and formatting the message
        with open("letter_templates/"+random.choice(txt_files_list)) as txt_file:
            txt = txt_file.read()
        message = txt.replace("[NAME]", name)
        message_object = EmailMessage()
        message_object["From"] = my_email
        message_object["To"] = ppl_to_be_emailed[name][0]
        message_object["subject"] = "🎂 Happy Birthday 🎂"
        message_object.set_content(message)

        # connecting to gmail server and sending the message
        new_connection = smtplib.SMTP("smtp.gmail.com", 587)
        new_connection.starttls()
        new_connection.login(user=my_email, password=pass_word)
        new_connection.sendmail(from_addr=my_email, to_addrs=ppl_to_be_emailed[name][0],msg=message_object.as_string())
        new_connection.close()







