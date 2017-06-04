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

#file handling
from os import listdir, remove
from os.path import isfile, basename, join as join_path


class Checker:
    def read(self, f):
        return BeautifulSoup(f, 'html.parser')

    def to_string(self, o):
        return o.prettify()

    def get_old_data(self, path):
        old_files = sorted([f for f in listdir(path) if isfile(join_path(path,f))], key=int)
        old_paths = [join_path(path, f) for f in old_files]
        old_data = []
        for p in old_paths:
            with open(p, 'r') as old_file:
                old_data.append(self.read(old_file)) 
            remove(p)
        return old_data

    def get_new_data(self, data, path):
        return data

    def save(self, path, data):
        for idx, snippet in enumerate(data):
            with open(join_path(path, str(idx)), 'w') as new_file:
                new_file.write(self.to_string(snippet))

    def check(self, name, url, data, dir_l, silent=False):
        data_old = self.get_old_data(dir_l)
        data_new = self.get_new_data(data, url)
        if not silent: self.notify(name, url, data_old, data_new)
        self.save(dir_l, data_new)


class Diff(Checker):
    def notify(self, name, url, data_old, data_new):
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
                Notify.init(name)
                n = Notify.Notification.new(name,msg)
                n.show()
        if l_new>l_old: #data has been added
            msg = 'Entries have been added:\n'
            for i in range(l_old,l_new):
                msg += data_new[i].prettify()
            print(name+':\n'+msg)
            Notify.init(tracker.name)
            n = Notify.Notification.new(tracker.name,msg)
            n.show()
        elif l_new<l_old: #data has been removed
            pass
            #TODO: maybe do something here


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
