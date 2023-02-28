from bs4 import BeautifulSoup
from typing import List, TypedDict

class ResultExtraction(TypedDict):
    date : str
    price : int

class EmailContentExtraction:
    def __init__(self) -> None:
        self.result_list : List[ResultExtraction] = []
        self.result_extraction : ResultExtraction = {}
        
    def add_data(self, html_content):
        new_data = BeautifulSoup(html_content, 'html.parser').findAll("p",{"class":"text-right"})
        date = new_data[1].find('strong').text.strip().split(',')[0] # '23 Feb 2023'
        price = new_data[4].find('strong').text.strip() # 'IDR 18,000'
        price_int = int(price.split()[1].replace(',',''))
        self.result_extraction = {'date':date,'price':price_int} 
        self.result_list.append(self.result_extraction)
