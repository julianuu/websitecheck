#from config import target_address #This does not work atm because we need to import this file into config.py and cant import it backe again I think

from bs4 import BeautifulSoup   # for HTML parsing
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

from difflib import unified_diff
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify #desktop notifications, requires python-gobject

import urllib.request  # for fetching files
from urllib.parse import quote

import re

#file handling
from os import listdir, remove
from os.path import isfile, basename, join as join_path, dirname


def empty(path):
    for p in [join_path(path,f) for f in listdir(path) if isfile(join_path(path,f))]:
        remove(p)

class Checker:
    def get_old_data(self, path):
        old_files = sorted([f for f in listdir(path) if isfile(join_path(path,f))], key=int)
        old_paths = [join_path(path, f) for f in old_files]
        old_data = []
        for p in old_paths:
            with open(p, 'r') as f: 
                old_data.append(BeautifulSoup(f, 'html.parser')) 
        return old_data

    def get_new_data(self, data, url):
        return data

    def save(self, path, data):
        for idx, snippet in enumerate(data):
            with open(join_path(path, str(idx)), 'w') as new_file:
                new_file.write(snippet.prettify())

    def check(self, name, url, data, dir_l, silent=False):
        data_old = self.get_old_data(dir_l)
        data_new = self.get_new_data(data, url)
        change = True
        if not silent: change = self.compare(name, url, data_old, data_new)
        if change:
            empty(dir_l)
            self.save(dir_l, data_new)

def dnotify(*args, **kwargs):
    Notify.init('websitecheck')
    n=Notify.Notification.new(*args, **kwargs)
    n.show()

class Diff(Checker):
    def compare(self, name, url, data_old, data_new):
        change = False
        l_old = len(data_old)
        l_new = len(data_new)
        l = min(l_old,l_new)
        for i in range(0,l):
            text_old = data_old[i].prettify().splitlines()
            text_new = data_new[i].prettify().splitlines()
            msg = ''
            o = 2
            i = 0
            for line in unified_diff(text_old, text_new, n=0):
                i+=1
                if i>o: #skip explanation/description of the diff
                    msg+=' '.join(line.split())+'\n' #remove all those tabs
            if i>o: #only notify if the strings actually differ
                print(name+':\n'+msg)
                dnotify(name,msg)
                change = True
        if l_new>l_old: #data has been added
            msg = 'Occurrences have been added:\n'
            for i in range(l_old,l_new):
                msg += data_new[i].prettify()
            print(name+':\n'+msg)
            dnotify(name,msg) #Idea: also open the saved file in webbrowser of choice. Thedesktpo notification is hardly readable if the change is big
            change = True
        elif l_new<l_old: #data has been removed
            pass
            #TODO: maybe do something here
        return change

    def __repr__(self):
        return 'Diff()'


class Filechange(Checker):
    def __init__(self, ftype):
        self.ftype = ftype

    def get_old_data(self, path):
        names = listdir(path)
        data = []
        for name in names:
            with open(join_path(path,name), 'rb') as f:
                data.append({'name':name, 'file':f.read(), 'removed':True})
        return data

    def get_new_data(self, data, url):
        new_data = []
        for soup in data:
            for tag in soup.findAll('a', href=re.compile('.*\.'+self.ftype)): #generalize so that the whole regex is a parameter of the class?
                link = quote(tag['href'], safe="%/:=&?~#+!$,;'@()*[]") #whitespaces, but so that quote doesn't change the ':' in 'http://…'
                name = basename(link)
                if not link.startswith('http'):
                    link = join_path(dirname(url),link)
                response = urllib.request.urlopen(link)
                new_data.append({'name':name, 'file':response.read(), 'new':True})
        return new_data
    
    def save(self, path, data):
        for entry in data:
            with open(join_path(path,entry['name']), 'wb') as new_file:
                new_file.write(entry['file'])
    
    def notify(self,name,text):
        print(name+': '+text)
        dnotify(name,text)
        self.change=True

    def compare(self, name, url, data_old, data_new): #missing: handle the case, that multiple files with the same name appear on the site
        self.change = False
        for file_old in data_old:
            for file_new in data_new:
                if file_old['name'] == file_new['name']:
                    file_old['removed'] = False
                    file_new['new'] = False
                    if file_old['file'] != file_new['file']:
                        self.notify(name,file_old['name'] + ' has changed.')
            if file_old['removed']:
                self.notify(name,file_old['name'] + ' has been removed.')
        for file_new in data_new:
            if file_new['new']:
                self.notify(name,file_new['name'] + ' has been added.')
        return self.change

    def __repr__(self):
        return('Filechange(' + self.ftype + ')')




def send_mail(tracker, plain = "", html = None, attachments = []):
    # Temporary solution to avoid using a local SMTP server.
    me = "websitecheck101@gmail.com"
    # Temporary ugliness to avoid commiting the password.
    passwd = getpass("Please enter password for websitecheck101@gmail.com: ")

    subject = 'Websitecheck: "' + tracker.name + '" has changed.'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Websitecheck: " + site["name"] + " has changed."
    msg['From'] = me
    msg['To'] = target_address

    part1 = MIMEText(plain, 'plain')
    msg.attach(part1)

    if isinstance(html, str):
        part2 = MIMEText(html, 'html')
        msg.attach(part2)

    #TODO: handle attachments

    # Connect to gmail.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(me, passwd)
    s.sendmail(me, target_address, msg.as_string())
    s.quit()

    print("Email sent.")    # for debugging purposes
