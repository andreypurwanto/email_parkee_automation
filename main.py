# Importing libraries
import imaplib
import mailparser
import imgkit
import os
from common.constant import (
    IMAP_URL, 
    START_SCRAP, 
    END_SCRAP, 
    EXCEL_NAME, 
    PATH_BASE_EXCEL, 
    MY_GMAIL, 
    MY_APP_PASSWORD, 
    CURRENT_MAX_ROW,
    DEFAULT_SUBJECT,
    DEFAULT_BODY_SUCCESS,
    DEFAULT_BODY_ERROR
)
from common.helpers import email_validation, str_to_datetime, send_email
from common.logger import LOG
from module.extraction import EmailContentExtraction
from module.editor import ExcelEditor
import shutil
import img2pdf

class EmailScrap:
    def __init__(self) -> None:
        self.receipt_name = 'receipt_zip'
        self.start_dt, self.end_dt = str_to_datetime(START_SCRAP, END_SCRAP)

        if not os.path.isdir(os.path.join(os.getcwd(),'result')):
            os.mkdir(os.path.join(os.getcwd(),'result'))
        else:
            # TODO handle this make unique then later delete
            shutil.rmtree(os.path.join(os.getcwd(),'result'), ignore_errors=False, onerror=None)
            os.mkdir(os.path.join(os.getcwd(),'result'))

        path_result = os.path.join(os.getcwd(), 'result')

        if not os.path.isdir(os.path.join(path_result,'receipt')):
            os.mkdir(os.path.join(path_result,'receipt'))

        self.path_result_image = os.path.join(path_result,'receipt')
        self.path_result_excel = os.path.join(path_result,f'{EXCEL_NAME}.xlsx')
        self.path_result_image_zip = os.path.join(path_result,f'{self.receipt_name}.zip')
        self.list_img_file = []

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
        try:
            self.config = imgkit.config()
            self.con = imaplib.IMAP4_SSL(IMAP_URL)

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
                            path_img_file = os.path.join(self.path_result_image,f'{mail.date.strftime("%m_%d_%Y-%H_%M_%S")}.jpg')
                            imgkit.from_string(mail_body_clean,path_img_file, config=self.config)
                            self.list_img_file.append(path_img_file)
                            email_extraction.add_data(mail_body_clean)
                            excel_editor.replace_value(email_extraction.result_extraction)
                            LOG.info(email_extraction.result_extraction)
                            count+=1
                        else:
                            LOG.info(f'different format')
                else :
                    LOG.info(f'EXCEED MAX ROW {email_extraction.result_extraction}')
                    # TODO need to handle body if exceeded max row, send warning start email 

            excel_editor.save_workbook(self.path_result_excel)
            self.res = email_extraction.result_list

            # zip
            shutil.make_archive(os.path.join('result',self.receipt_name), 'zip', self.path_result_image)
            
            # pdf
            # Convert the list of JPEG images to a single PDF file
            pdf_data = img2pdf.convert(self.list_img_file)

            # Write the PDF content to a file (make sure you have write permissions for the specified file)
            with open(os.path.join('result',"receipts.pdf"), "wb") as file:
                file.write(pdf_data)

            send_email(DEFAULT_SUBJECT, DEFAULT_BODY_SUCCESS,[MY_GMAIL],[self.path_result_excel, self.path_result_image_zip, os.path.join('result',"receipts.pdf")])
        except Exception as e:
            LOG.error(e, exc_info=True)
            send_email(DEFAULT_SUBJECT, DEFAULT_BODY_ERROR,[MY_GMAIL],None)

if __name__ == '__main__':
    LOG.info('start')
    EmailScrap().process()