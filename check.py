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

# Returns the absolute path of the directory in which snapshots of websites are stored.
# Right now this is "data/" relative to the path of the script.
def path_to_data_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "data")

# Returns the absolute path of the file in which snapshots of the given website are stored.
def path_to_file(site):
    return os.path.join(path_to_data_dir(), site["name"])

# Fetches the website and returns the relevant part as a BeautifulSoup object.
def fetch_new_data(site):
    html_doc = urllib.request.urlopen(site["url"])
    soup = BeautifulSoup(html_doc, 'html.parser')
    # So far we can only extract tags that have an id. May change this later.
    return soup.find(id=site["tag_id"]).prettify()

# Fetches the stored snapshot of a website.
def fetch_old_data(site):
    try:
        f = open(path_to_file(site))
        data = BeautifulSoup(f.read(), 'html.parser').prettify()
        f.close()
    except FileNotFoundError:
        data = ""
    return data

# Saves the given data as the new snapshot of a website
def store_data(site, data):
    f = open(path_to_file(site), "w")
    f.write(data)
    f.close()

# Notification function. Currently sends an email via some Gmail account.
def notify(site, old_data, new_data):
    if old_data == new_data:
        print("Did not change.")    # for debugging purposes
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

data_dir = path_to_data_dir()
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Temporary ugliness to avoid commiting the password.
passwd = getpass("Please enter password for websitecheck101@gmail.com: ")

notify_email = input("Please enter email address to notify: ") # Of course we may also change this.

for site in sites:
    
    # Display identifiers of tracked websites for debugging purposes
    print()
    print(site["name"] + ": ", end = '')

    old_data = fetch_old_data(site)
    new_data = fetch_new_data(site)

    notify(site, old_data, new_data)

    # Store new date (commented out for testing purposes)
    store_data(site, new_data)
