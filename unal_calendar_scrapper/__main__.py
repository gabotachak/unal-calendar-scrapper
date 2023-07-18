import json
from unal_calendar_scrapper.clients import UnalClient, GoogleCalendarClient


def main():
    unal_client = UnalClient()
    google_calendar_client = GoogleCalendarClient()

    calendars = unal_client.scrap_calendars()
    unal_client.close()

    for calendar in calendars:
        print("Processing calendar: {}".format(calendar.title))
        calendar.google_info = google_calendar_client.get_calendar_by_summary(
            calendar.title
        )

        if calendar.google_info is None:
            print("Creating calendar: {}".format(calendar.title))
            calendar.google_info = google_calendar_client.create_calendar(
                calendar.title
            )

        google_events = google_calendar_client.get_events_by_calendar_id(
            calendar.get_google("id")
        )

        for i, event in enumerate(calendar.events):
            print(
                "Processing event {} of {} for calendar {}".format(
                    i + 1, len(calendar.events), calendar.title
                )
            )
            matching_events = [
                e
                for e in google_events
                if e["summary"].lower() == event.activity.lower()
            ]
            event.google_info = matching_events[0] if matching_events else None

            if event.google_info is None:
                print(
                    "Creating event {} of {} for calendar {}".format(
                        i + 1, len(calendar.events), calendar.title
                    )
                )
                event.google_info = google_calendar_client.create_event(
                    calendar.get_google("id"), event
                )

            # TODO: Update event if it already exists


main()
