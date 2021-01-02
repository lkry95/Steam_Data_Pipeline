import smtplib
import os
from email.message import EmailMessage

def send_email():

    from_email_address = os.environ.get('steam_email')
    to_email_address = os.environ.get('email_address')
    email_password = os.environ.get('yahoo_password')

    msg = EmailMessage()
    msg['Subject'] = 'Daily Game Suggestions'
    msg['From'] = from_email_address
    msg['To'] = to_email_address

    msg.set_content('Here are your top picks!')

    with open('/Users/luke/PassionProject/LukesPicks.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype = 'text', subtype = 'txt', filename = file_name)


    #Context Manager closes connection automatically
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        #identifies mail server
        smtp.ehlo()
        #Encrypt traffic
        smtp.starttls()
        smtp.ehlo()

        #logs in to email server
        smtp.login(from_email_address,email_password)
        smtp.send_message(msg)
