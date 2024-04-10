import requests
import base64
import random

# to access API
client_id = '65a6e47f54f7483a9b40bf72d796bbb8'
client_secret = 'f1edc678de234c2a9c6d2c10bb1c9f00'

# gets the access token
def get_access_token(client_id, client_secret):

    client_creds = client_id + ":" + client_secret
    client_creds_b64 = base64.b64encode(client_creds.encode()) 
    #basically we need to encode the credentials in order for it to work with spotify API since the API expects this kind of format for client credentials

    token_data = {
        "grant_type": "client_credentials"
    }
    token_headers = {
        "Authorization": "Basic {}".format(client_creds_b64.decode())
        # .format puts decoded client_creds_b64 into the {}
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    if r.status_code in range(200, 299):
        return r.json()['access_token']
    return None

# gets random song from playlist
def get_random_song(access_token, playlist_id, choice='song'):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = requests.get('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id), headers=headers)
    if response.status_code in range(200, 299):
        playlist_tracks = response.json()['items']
        random_track = random.choice(playlist_tracks)
        if choice == 'song':
            item_name = random_track['track']['name']
            artist_name = random_track['track']['artists'][0]['name']
        elif choice == 'artist':
            item_name = random_track['track']['artists'][0]['name']      
            artist_name = None 
        else:
            return None, None
        return item_name, artist_name
    return None, None


# retrieves access token, code actually runs from here !!!
access_token = get_access_token(client_id, client_secret)

if access_token: #checks to see if we have access token
    choice = input("Enter 'song' to get a random song or 'artist' to get a random artist: ").lower()
    if choice in ['song','artist']:
        for i in range(5):
        # playlist ID from spotify
            playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
        # Get a random song
            item_name, artist_name = get_random_song(access_token, playlist_id, choice)
            if item_name and artist_name:
                if choice == 'song':
                    print("Random Song: {} by {}".format(item_name, artist_name))
                else:
                    print("Random Artist: {}".format(artist_name))
            else:
                print("Failed to fetch data from the playlist")
        else:
            print("Invalid choice. Please choose either 'song' or 'artist.")
    else:
        print("Failed to get access token")

  