# Importing libraries
import imaplib, email
import mailparser
from datetime import datetime
import imgkit
import os
from constant import *

config = imgkit.config(wkhtmltoimage=WKHTMLTOIMAMGE_PATH)

# Function to search for a key value pair
def search(key, value, con : imaplib.IMAP4_SSL):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data
 
# Function to get the list of emails under this label
def get_emails(con : imaplib.IMAP4_SSL, result_bytes):
    msgs = [] # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs

def email_validation(em : str) -> bool:
    if 'Ticket' or 'ticket' in email:
        return True
    return False

def str_to_datetime(start : str, end:str) -> tuple[datetime,datetime]:
    if end == 'now':
        end = datetime.now()
    else : 
        end = datetime.strptime(start, r'%d_%m_%y')
    start = datetime.strptime(start, r'%d_%m_%y')
    return (start, end)

def start():
    start_dt, end_dt = str_to_datetime(START_SCRAP, END_SCRAP)

    if not os.path.isdir(os.path.join(os.getcwd(),'result')):
        os.mkdir(os.path.join(os.getcwd(),'result'))

    path_result = os.path.join(os.getcwd(), 'result')

    if not os.path.isdir(os.path.join(path_result,'image')):
        os.mkdir(os.path.join(path_result,'image'))

    path_result_image = os.path.join(path_result,'image')

    # this is done to make SSL connection with GMAIL
    con = imaplib.IMAP4_SSL(IMAP_URL)

    # logging the user in
    con.login(MY_GMAIL, MY_APP_PASSWORD)
    
    # calling function to check for email under this label
    con.select('Inbox')
    
    # fetching emails from this user "tu**h*****1@gmail.com"
    msgs = get_emails(con, search('FROM', 'hello@parkee.app', con))

    for msg in reversed(msgs):
        mail = mailparser.parse_from_bytes(msg[0][1]) 
        if end_dt > mail.date > start_dt:
            print(mail.date)
            word_to_exclude_after = '--- mail_boundary ---'
            mail_body_clean = mail.body[mail.body.index(word_to_exclude_after)+len(word_to_exclude_after):]
            if email_validation(mail_body_clean):
                imgkit.from_string(mail_body_clean,os.path.join(path_result_image,f'{mail.date.strftime("%m_%d_%Y-%H_%M_%S")}.jpg'), config=config)

if __name__ == '__main__':
    start()