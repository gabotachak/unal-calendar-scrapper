import re
import dateparser

from datetime import date
from typing import Tuple


def str_date_to_dates(str_date: str) -> Tuple[date, date]:
    str_date = str_date.lower()
    single_date = dateparser.parse(str_date)
    if single_date is not None:
        return single_date.date(), single_date.date()
    
    start_date, end_date = None, None
    if "desde el" in str_date:
        str_date = str_date.split("desde el")[-1]
        try:
            str_start_date = re.search(r"\d{2}[A-Za-z ]*\d{4}", str_date).group(0)
            start_date = dateparser.parse(str_start_date).date()
        except AttributeError:
            pass
        
    if "hasta el" in str_date:
        str_date = str_date.split("hasta el")[-1]
        try:
            str_end_date = re.search(r"\d{2}[A-Za-z ]*\d{4}", str_date).group(0)
            end_date = dateparser.parse(str_end_date).date()
        except AttributeError:
            pass
        
    return (start_date, end_date)

class UnalEvent:
    activity: str = None
    responsable: str = None
    start_date: date = None
    end_date: date = None
    
    def __init__(self, activity:str, responsible: str, str_date: str=None) -> None:
        self.activity = activity
        self.responsable = responsible
        
        if str_date is not None:
            self.start_date, self.end_date = str_date_to_dates(str_date)
    
    def __str__(self) -> str:
        return f"Activity: {self.activity}, responsable: {self.responsable}, start_date: {self.start_date}, end_date: {self.end_date}"
        
        
    
    