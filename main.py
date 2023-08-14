# Importing libraries
import imaplib
import mailparser
import imgkit
import os
from common.constant import *
from common.helpers import email_validation, str_to_datetime
from common.logger import LOG
from module.extraction import EmailContentExtraction
from module.editor import ExcelEditor

class EmailScrap:
    def __init__(self) -> None:
        # self.config = imgkit.config(wkhtmltoimage=WKHTMLTOIMAMGE_PATH)
        self.config = imgkit.config()
        self.con = imaplib.IMAP4_SSL(IMAP_URL)
        self.start_dt, self.end_dt = str_to_datetime(START_SCRAP, END_SCRAP)

        if not os.path.isdir(os.path.join(os.getcwd(),'result')):
            os.mkdir(os.path.join(os.getcwd(),'result'))

        path_result = os.path.join(os.getcwd(), 'result')

        if not os.path.isdir(os.path.join(path_result,'image')):
            os.mkdir(os.path.join(path_result,'image'))

        self.path_result_image = os.path.join(path_result,'image')

        if not os.path.isdir(os.path.join(path_result,'excel')):
            os.mkdir(os.path.join(path_result,'excel'))

        self.path_result_excel = os.path.join(path_result,'excel',f'{EXCEL_NAME}.xlsx')

    # Function to search for a key value pair
    def search(self, key, value):
        _, data = self.con.search(None, key, '"{}"'.format(value))
        return data
    
    # Function to get the list of emails under this label
    def get_emails(self, result_bytes):
        msgs = [] # all the email data are pushed inside an array
        for num in result_bytes[0].split():
            _, data = self.con.fetch(num, '(RFC822)')
            msgs.append(data)
        return msgs

    def process(self):
        email_extraction = EmailContentExtraction()
        excel_editor = ExcelEditor(path=PATH_BASE_EXCEL)
        
        # logging the user in
        self.con.login(MY_GMAIL, MY_APP_PASSWORD)
        
        # calling function to check for email under this label
        self.con.select('Inbox')
        
        # fetching emails
        msgs = self.get_emails(self.search('FROM', 'hello@parkee.app'))
        count = 0
        for msg in msgs:
            if count < CURRENT_MAX_ROW:
                mail = mailparser.parse_from_bytes(msg[0][1]) 
                if self.end_dt > mail.date > self.start_dt:
                    LOG.info(mail.date)
                    word_to_exclude_after = '--- mail_boundary ---'
                    mail_body_clean = mail.body[mail.body.index(word_to_exclude_after)+len(word_to_exclude_after):]
                    if email_validation(mail_body_clean):
                        imgkit.from_string(mail_body_clean,os.path.join(self.path_result_image,f'{mail.date.strftime("%m_%d_%Y-%H_%M_%S")}.jpg'), config=self.config)
                        email_extraction.add_data(mail_body_clean)
                        excel_editor.replace_value(email_extraction.result_extraction)
                        LOG.info(email_extraction.result_extraction)
                        count+=1
                    else:
                        LOG.info(f'different format')
            else :
                LOG.info(f'EXCEED MAX ROW {email_extraction.result_extraction}')
        excel_editor.save_workbook(self.path_result_excel)
        self.res = email_extraction.result_list

if __name__ == '__main__':
    LOG.info('start')
    EmailScrap().process()