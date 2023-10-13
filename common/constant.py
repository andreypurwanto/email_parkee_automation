import os
from dotenv import load_dotenv

load_dotenv()

MY_GMAIL = os.getenv('MY_GMAIL')
MY_APP_PASSWORD = os.getenv('MY_APP_PASSWORD')
IMAP_URL = 'imap.gmail.com'
START_SCRAP = '13_07_23' # DD_MM_YY
END_SCRAP = 'now'
WKHTMLTOIMAMGE_PATH = os.path.join(os.getcwd(),'wkhtmltox','bin','wkhtmltoimage.exe')
CURRENT_MAX_ROW = 27

COLUMN_DATE = 'B'
COLUMN_EXPLANATION = 'C'
COLUMN_COST = 'G'
EXPLANATION_NARRATION = 'Motorcycle Parking WFO (Dipo Tower)'
START_ROW = 15
CELL_NAME = 'C9'
CELL_SIGNATURE_NAME = 'C51'
CELL_DATE = 'F10'

PATH_BASE_EXCEL = os.path.join(os.getcwd(),'static','FinAccel_ExpenseClaim_Base.xlsx')

NAME = 'Andrey Purwanto'

EXCEL_NAME_IDENTIFIER = NAME.replace(' ','')
EXCEL_BASE_NAME = 'FinAccel_Expense_Claim'
EXCEL_NAME = f'{EXCEL_BASE_NAME}_{EXCEL_NAME_IDENTIFIER}'

BOT_SENDER_EMAIL = os.getenv('BOT_SENDER_EMAIL')
BOT_SENDER_PASSWORD = os.getenv('BOT_SENDER_PASSWORD')

DEFAULT_SUBJECT = "Your Parkee Extraction"
DEFAULT_BODY_SUCCESS = "Success"
DEFAULT_BODY_ERROR = "There is an error for your extraction, please make sure you already use App Password. If Issue persist, contact administrator."