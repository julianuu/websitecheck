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

from os import listdir
from os.path import join, isfile   # for determining file and directory paths

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
    def __init__(self, name, url, actions):
        self.name = name
        self.url = url
        self.actions = actions
    
    def check(self):
        with urllib.request.urlopen(self.url) as response:
            new_data = [BeautifulSoup(response, 'html.parser')]

        self.__iterate__(new_data, [], self.actions)


    def __iterate__(data, selectionsDone, actionsPending):
        if len(actionsPending) == 0:
            return

        actions = actionsPending[0]
        if not isinstance(actions, list):
            actions = [actions]

        appended = False
        
        for action in actions:
            if isinstance(a, Selector):
                my_data = a.select(data)
                selectionsDone.append(action)
            elif isinstance(a, Notifier):
                my_data = data

                selstr = '.'.join(list(map(lambda a: repr(a), actions)))
                old_dir = os.path.join(cache_dir, self.url.replace("/", "%2F"), selstr)

                old_paths = sorted([f for f in listdir(old_dir) if isfile(join(old_dir,f))], key=int)
                old_data = []
                for p in old_paths:
                    with open(p, 'r') as old_file:
                        old_data.append(BeautifulSoup(old_file.read(), 'html.parser'))

                a.notify(self, new_data, old_data)

                # TODO: Save acquired data.

            self.__iterate__(my_data, selectionsDone, actionsPending[:-1])
            if appended:
                actionsDone.pop()
