from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from unal_calendar_scrapper.entities import UnalCalendar
from unal_calendar_scrapper.entities import UnalEvent

UNAL_URL = "https://bogota.unal.edu.co/calendario-academico/"

class UnalClient:
    def __init__(self) -> None:
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)

    def scrap_calendars(self) -> List[UnalCalendar]:
        print("Initializing scrapping...")
        self.driver.get(UNAL_URL)
        calendars: List[UnalCalendar] = []

        sections = self.driver.find_elements("xpath", "//div[@class='csc-default']")
        print("Found {} sections".format(len(sections)))

        for section in sections:
            try:
                table = section.find_element(
                    "xpath",
                    ".//div[@class='dataTables_wrapper dt-bootstrap4 no-footer']",
                )
            except NoSuchElementException:
                continue

            title = section.find_element("xpath", ".//h1").text
            print("Found section: {}".format(title))

            new_calendar = UnalCalendar(title)

            ## search the select which controls the number of rows per page and select the max value
            select_element = table.find_element("xpath", ".//select")
            page_select = Select(select_element)
            max_option = -1
            for option in page_select.options:
                if int(option.text) > max_option:
                    max_option = int(option.text)

            page_select.select_by_value(str(max_option))

            # search the pagination buttons and click them all one by one
            pag_buttons = table.find_elements(
                "xpath",
                ".//li[@class='paginate_button page-item ' or @class='paginate_button page-item active']",
            )
            pag_buttons_not_clicked = {pag_button.text for pag_button in pag_buttons}

            while pag_buttons_not_clicked:
                pag_buttons = table.find_elements(
                    "xpath",
                    ".//li[@class='paginate_button page-item ' or @class='paginate_button page-item active']",
                )
                for pag_button in pag_buttons:
                    if pag_button.text in pag_buttons_not_clicked:
                        pag_buttons_not_clicked.remove(pag_button.text)
                        self.driver.execute_script("arguments[0].click();", pag_button)
                        break

                # search the rows by pagination and extract the data
                rows = table.find_elements(
                    "xpath", ".//tr[@role='row' and (@class='even' or @class='odd')]"
                )
                for row in rows:
                    elements = row.find_elements("xpath", ".//td")
                    date, activity, description = [element.text for element in elements]
                    new_calendar.add_event(
                        UnalEvent(activity, description, str_date=date)
                    )

            calendars.append(new_calendar)

        print("Ended scrapping.")
        return calendars

    def close(self) -> None:
        self.driver.close()
