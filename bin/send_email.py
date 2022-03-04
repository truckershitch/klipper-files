# send_email.py
# Helper script to send emails
#
# Created February 21, 2022
# Modified February 21, 2022

import smtplib
from klipper_email_cfg import *

def send_mail(email_body):
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', port=587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()

        smtpObj.login(GMAIL_USER, GMAIL_PASS)
        smtpObj.sendmail(DEST_EMAIL, DEST_EMAIL, email_body)

        print('Email sent.')
    except smtplib.SMTPException as e:
        print('Error: unable to send email: %s' % e)