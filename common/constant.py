import os
from dotenv import load_dotenv

load_dotenv()

MY_GMAIL = os.getenv('MY_GMAIL')
MY_APP_PASSWORD = os.getenv('MY_APP_PASSWORD')
IMAP_URL = 'imap.gmail.com'
START_SCRAP = '01_02_23'
END_SCRAP = 'now'
WKHTMLTOIMAMGE_PATH = os.path.join(os.getcwd(),'wkhtmltox','bin','wkhtmltoimage.exe')