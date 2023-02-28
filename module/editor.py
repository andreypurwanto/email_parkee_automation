from openpyxl import load_workbook
import os
from typing import TypedDict
from common.constant import *
from datetime import date

class ResultExtraction(TypedDict):
    date : str
    price : int

class ExcelEditor:
    def __init__(self,path):
        self.workbook = load_workbook(filename=path)
        self.sheet = self.workbook.active
        self.cur_row = START_ROW
        self.sheet[CELL_NAME] = NAME
        self.sheet[CELL_SIGNATURE_NAME] = NAME
        self.sheet[CELL_DATE] = str(date.today())

    def replace_value(self, value : ResultExtraction):
        self.sheet[str(COLUMN_DATE)+str(self.cur_row)] = value['date']
        self.sheet[str(COLUMN_EXPLANATION)+str(self.cur_row)] = EXPLANATION_NARRATION
        self.sheet[str(COLUMN_COST)+str(self.cur_row)] = value['price']
        self.cur_row +=1  
    
    def save_workbook(self, path):
        self.workbook.save(filename=path)
