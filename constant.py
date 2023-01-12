import os
from dotenv import load_dotenv

load_dotenv()

MY_GMAIL = os.getenv('MY_GMAIL')
MY_APP_PASSWORD = os.getenv('MY_APP_PASSWORD')
IMAP_URL = 'imap.gmail.com'
START_SCRAP = '01_01_23'
END_SCRAP = 'now'
WKHTMLTOIMAMGE_PATH = os.getenv('WKHTMLTOIMAMGE_PATH')