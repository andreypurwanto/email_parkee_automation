from datetime import datetime

def email_validation(em : str) -> bool:
        if ('Ticket' in em) or ('ticket' in em):
            return True
        return False

def str_to_datetime(start : str, end:str) -> tuple[datetime,datetime]:
    if end == 'now':
        end = datetime.now()
    else : 
        end = datetime.strptime(start, r'%d_%m_%y')
    start = datetime.strptime(start, r'%d_%m_%y')
    return (start, end)