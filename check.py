#!/usr/bin/python3

'''
    Websitecheck

    Use Python 3.
    
'''

import os   # for determining file and directory paths
import urllib.request   # for fetching websites
'''
    BeautifulSoup is not in the Python standard library.
    Need to install python-beautifulsoup4 in Arch Linux.
'''
from bs4 import BeautifulSoup   # for HTML parsing
from difflib import HtmlDiff    # for creating nice visual diffs

# for email functionality:
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from getpass import getpass # for entering passwords

from websites import sites  # import list of tracked websites

'''
    ================
    Functions
    ================
'''


# Notification function. Currently sends an email via some Gmail account.
def notify(site, old_data, new_data):
    if old_data == new_data:
        return

    me = "websitecheck101@gmail.com"
    you = notify_email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Websitecheck: " + site["name"] + " has changed."
    msg['From'] = me
    msg['To'] = you

    text = "(Alternative text.)"    # to be improved, e.g. use difflib's context_diff or similar
    html = HtmlDiff().make_file(old_data.splitlines(True), new_data.splitlines(True), context=True, numlines=5)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    msg.attach(part1)
    msg.attach(part2)

    # Connect to gmail.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(me, passwd)

    s.sendmail(me, you, msg.as_string())
    s.quit()

    print("Email sent.")    # for debugging purposes

'''
    ===============
    Main script
    ===============
'''


# Temporary ugliness to avoid commiting the password.
passwd = getpass("Please enter password for websitecheck101@gmail.com: ")

notify_email = input("Please enter email address to notify: ") # Of course we may also change this.

for site in sites:
    
    # Display identifiers of tracked websites for debugging purposes
    print()
    print(site["name"] + ": ", end = '')

    site.check()

