import requests
import oauth
import json

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

    # Read google album id from google_ids.json
    with open(GOOGLE_ID_FILE, "r") as f:
        ids = json.loads(f.read())
        album_id = ids['album_id']

    # Call the Photos Library API
    print('Getting the photos album')

    headers = {"Authorization": token}
    body = {"albumId": album_id}

    r = requests.request("POST", f"https://photoslibrary.googleapis.com/v1/mediaItems:search",
                         headers=headers, data=body)
    if r.ok:
        album = r.json()
        for pic in album['mediaItems']:
            print(pic)
    else:
        print(r.text)
        print("Error getting pics from album")


if __name__ == '__main__':
    main()
