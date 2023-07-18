from unal_calendar_scrapper.entities.Event import UnalEvent
from typing import List


class UnalCalendar:
    title: str = None
    events: List[UnalEvent] = None
    google_info: dict = None

    def __init__(self, title: str) -> None:
        self.title = title

    def add_event(self, event: UnalEvent) -> None:
        if self.events is None:
            self.events = []

        self.events.append(event)

    def get_google(self, key: str, default: str = None) -> str:
        return self.google_info.get(key, default)
