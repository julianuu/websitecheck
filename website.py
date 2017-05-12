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

import re

class Notification:
    def __init__(self):
        self.change = False
        self.text = ''
        self.html = ''
   
def get_content_by_id(html,tag_id):
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
    def __init__(self, tag):
        self.tag = tag

    def soup_find(self, soup,tag_id):
        return soup.find(id=tag_id)

    def get_by_tag(self, html,tag_info):
        soup = BeautifulSoup(html, 'html.parser')
        tag = self.soup_find(soup, tag_info)
        if tag:
            content = tag.prettify()
        else:
            content = ''
        return content

    def filter_relevant(self,data):
        return self.get_by_tag(data, self.tag)

    def difference(self,old,new):
        notification = Notification()
        if old != new:
            #diff would be nicer
            notification.text = new    # to be improved, e.g. use difflib's context_diff or similar
            notification.change = True

        return notification

    def compare(self):
        old_data = self.filter_relevant(self._html_doc_old)
        new_data = self.filter_relevant(self._html_doc_new)
        return self.difference(old_data, new_data)

    def check(self, html_doc_new, html_doc_old, folder):
        self._html_doc_new = html_doc_new
        self._html_doc_old = html_doc_old
        #pdfcheck needs a directory where it can store the pdfs
        self._folder = folder

        return self.compare()
 
class Check_tag_name(Check):
    def soup_find(self,soup,tag_name):
        return soup.find(tag_name)

class Tag_check_htmldiff(Check):
    def difference(self, old,new):
        notification = Notification()
        notification.html = HtmlDiff().make_file(old.splitlines(True), new.splitlines(True), context=True, numlines=5)
        if old != new:
            #diff would be nicer
            notification.text = new    # to be improved, e.g. use difflib's context_diff or similar
            notification.change = True

        return notification

#look for links to pdf within tag, check them for change
def find_pdflinks(html):
    soup = BeautifulSoup(html, 'html.parser')
    pdflink_tags = soup.find_all(re.compile('([^/]/)*[^/]*\.pdf'))
    pdflinks = []
    for tag in pdflink_tags:
        link = tag['href']
        #find the *.pdf and call it 'name'
        match = re.search('([^/]/)*(?P<name>[^/]*\.pdf)',link)
        pdflinks.append([match.group['name'], name])
    return pdflinks


class Pdfs_check(Check):
    def difference(self, old, new):
        pdflinks_old = find_pdflinks(old)
        pdflinks_new = find_pdflinks(new)
        return Notification()

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


class Tracker:
    def __init__(self, name, url, selectors, notifier):
        self.name = name
        self.url = url
        self.selectors = selectors
        self.notifier = notifier

    def check(self):
        with urllib.request.urlopen(self.url) as response:
            new_data = BeautifulSoup(response, 'html.parser')

        for s in selectors:
            new_data = s[1](new_data)

        selstr = selectors_to_string(selectors)
        my_cache_dir = os.path.join(cache_dir, self.url.replace("/", "%2F"), selstr)

        notifier(this, new_data, my_cache_dir)
