import re
import dateparser

from datetime import date
from typing import Tuple


class UnalEvent:
    activity: str = None
    description: str = None
    start_date: date = None
    end_date: date = None
    google_info: dict = None

    def __init__(self, activity: str, description: str, str_date: str = None) -> None:
        self.activity = activity
        self.description = description

        if str_date is not None:
            self._str_date_to_dates(str_date)
            
    def _str_date_to_dates(self, str_date: str) -> None:
        str_date = str_date.lower()
        single_date = dateparser.parse(str_date)
        if single_date is not None:
            self.start_date, self.end_date = single_date.date(), single_date.date()

        if "desde el" in str_date:
            str_date = str_date.split("desde el")[-1]
            try:
                str_start_date = re.search(r"\d{2}[A-Za-z ]*\d{4}", str_date).group(0)
                self.start_date = dateparser.parse(str_start_date).date()
            except AttributeError:
                pass

        if "hasta el" in str_date:
            str_date = str_date.split("hasta el")[-1]
            try:
                str_end_date = re.search(r"\d{2}[A-Za-z ]*\d{4}", str_date).group(0)
                self.end_date = dateparser.parse(str_end_date).date()
            except AttributeError:
                pass
            
        # There is no date information
        if self.start_date is None and self.end_date is None:
            return
        
        if self.start_date is None:
            self.activity = f"Límite para {self.activity}"
            self.start_date = self.end_date
            
        if self.end_date is None:
            self.activity = f"Inicio de {self.activity}"
            self.end_date = self.start_date

    def get_google(self, key: str, default: str = None) -> str:
        return self.google_info.get(key, default)
