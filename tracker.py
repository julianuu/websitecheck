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

import re   # regular expressions

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
        tracker_cache_dir = os.path.join(cache_dir, self.url.replace("/", "%2F"), selstr)

        notifier(this, new_data, tracker_cache_dir)
