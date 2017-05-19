from websites import target_address

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify():
        pass

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
