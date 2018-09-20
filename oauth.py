from oauth2client import file, client, tools
import requests
import json

TOKEN_FILE = "token.json"
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/photoslibrary'
]


def google_authorize():
    store = file.Storage(TOKEN_FILE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        credentials = tools.run_flow(flow, store)


def test_access_token():
    with open(TOKEN_FILE, "r") as f:
        credentials = json.loads(f.read())
    # Test access token
    r = requests.request("POST",
                         f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={credentials['access_token']}")
    # If token does not work refresh token
    if not r.ok:
        params = {
            "client_id": credentials['client_id'],
            "client_secret": credentials['client_secret'],
            "grant_type": "refresh_token",
            "refresh_token": credentials['refresh_token']
        }
        r = requests.request("POST", "https://www.googleapis.com/oauth2/v3/token", params=params)
        if r.ok:
            r = r.json()
            # Write new refresh token to TOKEN_FIlE
            credentials['access_token'] = r['access_token']
            with open(TOKEN_FILE, "w") as f:
                f.write(json.dumps(credentials))
