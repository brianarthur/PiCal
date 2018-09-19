from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the current months events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Get start and end months
    today = datetime.datetime.today()
    start_month = datetime.datetime(today.year, today.month, 1).isoformat() + 'Z' # 'Z' indicates UTC time
    if today.month == 12:
    	end_month = datetime.datetime(today.year + 1, 1, 1).isoformat() + 'Z'
    else:
    	end_month = datetime.datetime(today.year, today.month + 1, 1).isoformat() + 'Z'

    # Get google calendar id from text file: calendar_id.txt
    with open('calendar_id.txt', 'r') as f:
	calendar_id = f.read().splitlines()[0]
    
    # Call the Calendar API
    print('Getting the current months upcoming events')
    events_result = service.events().list(calendarId=calendar_id, timeMin=start_month,
                                        timeMax=end_month, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Print results
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()
