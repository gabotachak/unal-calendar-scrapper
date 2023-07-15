from unal_calendar_scrapper.clients import UnalClient


def main():
    unal_client = UnalClient()
    calendars = unal_client.scrap_calendars()
    print("Found {} calendars".format(len(calendars)))
    
main()