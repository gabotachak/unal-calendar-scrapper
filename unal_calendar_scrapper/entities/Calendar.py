from unal_calendar_scrapper.entities.Event import UnalEvent
from typing import List

class UnalCalendar:
    title: str = None
    events: List[UnalEvent] = None
    
    def __init__(self, title: str) -> None:
        self.title = title
        
    def __str__(self) -> str:
        return f"Calendar: {self.title}, events: {[str(e) for e in self.events]}"
    
    def add_event(self, event: UnalEvent) -> None:
        if self.events is None:
            self.events = []
            
        self.events.append(event)