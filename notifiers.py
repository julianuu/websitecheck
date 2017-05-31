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

class Notifier:
    def notify(self, name, url, sels, old_data, new_data):
        raise NotImplementedError("Please implement this method")

class Diff(Notifier):
    def notify(self, name, url, sels, data_old, data_new):
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
