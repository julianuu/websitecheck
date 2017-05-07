'''
    Right now this is just a sample configuration:
    It tracks the course website of Pavel's Weighted inequalities
    while ignoring Peter Scholze's newest awards.
'''
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

import os   # for determining file and directory paths

class Notification:
    def __init__(self):
        self.text = ''
        self.html = ''
   
def get_tag_content(html,tag_id):
    soup = BeautifulSoup(html, 'html.parser')
    #does not work at empty input:
    #content = soup.find(id=tag_id).prettify()
    tag = soup.find(id=tag_id)
    if tag:
        content = tag.prettify()
    else:
        content = ''

    return content

#standard check type, i.e. checking change within a tag
class Check:
    def __init__(self, tag_id):
        self._tag_id = tag_id

    def compare(self):
        old_data = get_tag_content(self._html_doc_old, self._tag_id)
        new_data = get_tag_content(self._html_doc, self._tag_id)

        notification = Notification()
        notification.text = new_data    # to be improved, e.g. use difflib's context_diff or similar

#diff would be nicer
        if old_data != new_data:
            notification.change = True

        return notification

    def check(self, html_doc, html_doc_old, folder):
        self._html_doc = html_doc
        self._html_doc_old = html_doc_old
        #pdfcheck needs a directory where it can store the pdfs
        self._folder = folder

        return self.compare()
 
class Tag_check_htmldiff(Check):
    def compare(self):
        old_data = get_tag_content(self._html_doc_old, self._tag_id)
        new_data = get_tag_content(self._html_doc, self._tag_id)

        notification = Notification()
        notification.text = new_data    # to be improved, e.g. use difflib's context_diff or similar
        notification.html = HtmlDiff().make_file(old_data.splitlines(True), new_data.splitlines(True), context=True, numlines=5)

#diff would be nicer
        if old_data != new_data:
            notification.change = True

        return notification


#look for links to pdf within tag, check them for change
class Pdfs_check(Check):
    def __init__(self, tag_id):
        self._tag_id = tag_id

#simple standard notification
class Notifier:
    def notify(self, name, notification):
        print(name+": "+notification.text)


#notify_email = input("Please enter email address to notify: ") # Of course we may also change this.

class Mail_notifier:
    def __init__(self,you):
        self.you = you

    def notify(self, name, notification):
        me = "websitecheck101@gmail.com"
        # Temporary ugliness to avoid commiting the password.
        passwd = getpass("Please enter password for websitecheck101@gmail.com: ")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Websitecheck: " + site["name"] + " has changed."
        msg['From'] = me
        msg['To'] = you

        part1 = MIMEText(notification.text, 'plain')
        part2 = MIMEText(notification.html, 'html')

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

#to store the html file. Checks take care of their data themselves if necessary. Except clearly every check needs the html file
def store_data(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()

def fetch_old_data(filename):
    try:
        f = open(filename)
        doc = f.read()
        f.close()
    except FileNotFoundError: 
        doc = ''

    return doc


class Website:
    def __init__(self, name, url, checks, notifiers):
        self.name = name
        self.url = url
        #list of checks to be performed for this website
        self.checks = checks
        self.notifiers = notifiers

    def check(self,folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.folder = folder
        self._html_name = os.path.join(self.folder,'index.html')
        with urllib.request.urlopen(self.url) as response:
            self._html_doc = response.read()
        self._html_doc_old = fetch_old_data(self._html_name)

        notification=""

        i=0

        for check in self.checks:
            #directory for every check in case if they need one
            change = False
            checkfolder = os.path.join(self.folder,str(i))
            notification = check.check(self._html_doc, self._html_doc_old, checkfolder)
            i+=1 
            if notification.change:
                change = True
            for notifier in self.notifiers:
                notifier.notify(self.name, notification)

            if change:
                store_data(self._html_name,self._html_doc)