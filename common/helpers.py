from datetime import datetime
from common.logger import LOG
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from common.constant import BOT_SENDER_EMAIL, BOT_SENDER_PASSWORD

def email_validation(em : str) -> bool:
    LOG.info('email_validation')
    if ('Ticket' in em) or ('ticket' in em):
        return True
    return False

def str_to_datetime(start : str, end:str):
    LOG.info('str_to_datetime')
    if end == 'now':
        end = datetime.now()
    else : 
        end = datetime.strptime(start, r'%d_%m_%y')
    start = datetime.strptime(start, r'%d_%m_%y')
    return (start, end)

def send_email(subject, body, recipients, filenames):
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = BOT_SENDER_EMAIL
    msg['To'] = ', '.join(recipients)
    if filenames:
        for filename in filenames:
            base_name = os.path.basename(filename)
            LOG.info(base_name)
            attach_file = open(filename, 'rb') # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream', Name=base_name)
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) #encode the attachment
            #add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=base_name)
            msg.attach(payload)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(BOT_SENDER_EMAIL, BOT_SENDER_PASSWORD)
       smtp_server.sendmail(BOT_SENDER_EMAIL, recipients, msg.as_string())
    LOG.info("Message sent!")