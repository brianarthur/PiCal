import datetime
import requests
import json
import oauth

TOKEN_FILE = "token.json"
GOOGLE_ID_FILE = "google_ids.json"


def main():
    # Only need for initializing access to new scopes
    oauth.google_authorize()

    # Test if access token is active / refresh token if expired
    oauth.test_access_token()

    # Read credentials from token.json file
    with open(TOKEN_FILE, "r") as f:
        credentials = json.loads(f.read())
        token = f"Bearer {credentials['access_token']}"

    # Read google calendar id from google_ids.json
    with open(GOOGLE_ID_FILE, "r") as f:
        ids = json.loads(f.read())
        calendar_id = ids['calendar_id']

    # Get start and end of month
    today = datetime.datetime.today()
    start_month = datetime.datetime(today.year, today.month, 1).isoformat() + 'Z'  # 'Z' indicates UTC time
    if today.month == 12:
        end_month = datetime.datetime(today.year + 1, 1, 1).isoformat() + 'Z'
    else:
        end_month = datetime.datetime(today.year, today.month + 1, 1).isoformat() + 'Z'

    # Call the Google Calendar API
    print('Getting calendar events')

    headers = {"Authorization": token}
    params = {
        "timeMin": start_month,
        "timeMax": end_month,
        "orderBy": 'startTime',
        "singleEvents": True
    }

    r = requests.request("GET", f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events",
                         headers=headers, params=params)
    if r.ok:
        events = r.json()
        for event in events['items']:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    else:
        print(r.text)
        print("Error getting events in calendar")


if __name__ == '__main__':
    main()
