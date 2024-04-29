import requests
import base64
import random

client_id = '65a6e47f54f7483a9b40bf72d796bbb8'
client_secret = 'f1edc678de234c2a9c6d2c10bb1c9f00'

# Written by partners
def get_access_token(client_id, client_secret):

    client_creds = client_id + ":" + client_secret
    client_creds_b64 = base64.b64encode(client_creds.encode()) 

    token_data = {
        "grant_type": "client_credentials"
    }
    token_headers = {
        "Authorization": "Basic {}".format(client_creds_b64.decode())
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    if r.status_code in range(200, 299):
        return r.json()['access_token']
    return None

# Written by partners
def get_random_song(playlist_id, choice):
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
            item_name = None      
            artist_name = random_track['track']['artists'][0]['name']
        return item_name, artist_name
    return None, None

# I wrote this part
def get_playlist_details(access_token, playlist_id):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = requests.get('https://api.spotify.com/v1/playlists/{}'.format(playlist_id), headers=headers)
    if response.status_code in range(200, 299):
        playlist_data = response.json()
        playlist_name = playlist_data['name']
        number_of_tracks = playlist_data['tracks']['total']
        return playlist_name, number_of_tracks
    return None, None
  
# I wrote this part
def print_playlist_info(access_token, plists):
  for playlist_id in plists:
      playlist_name, _ = get_playlist_details(access_token, playlist_id)
      if playlist_name:
          print("Playlist Name: {}, Playlist ID: {}".format(playlist_name, playlist_id))
      else:
          print("Failed to fetch details for Playlist ID: {}".format(playlist_id))


access_token = get_access_token(client_id, client_secret)
playlist_id = '37i9dQZF1DXcBWIGoYBM5M'

plists = [
  "37i9dQZF1DXcBWIGoYBM5M",
  "37i9dQZF1DWYBO1MoTDhZI",
  "37i9dQZF1DX0jgyAiPl8Af"
]

if access_token:
    while True:
        print("\nEnter 'song' to get a random song from the current playlist")
        print("Enter 'artist' to get a random artist from the current playlist")
        print("Enter 'playlist' to change the current playlist")
        print("Enter 'add' to add more playlists to the current list")
        choice = input("Enter anything else to quit: ").lower()
        if choice in ['song','artist']:
            for i in range(5):   
                item_name, artist_name = get_random_song(playlist_id, choice)
                if item_name and artist_name:
                    print("Random Song: {} by {}".format(item_name, artist_name))
                elif artist_name:
                    print("Random Artist: {}".format(artist_name))

        elif choice in ['playlist']:
            name, tracks = get_playlist_details(access_token, playlist_id)
            print("Previous Playlist: {} with {} songs. ID: {}".format(name, tracks,playlist_id))
            print("\n Playlists to choose from:")
            print_playlist_info(access_token, plists)
      
            play = input("enter the new playlist ID.")
            playlist_id = play
            name, tracks = get_playlist_details(access_token, play)
            print("Selected Playlist: {} with {} songs".format(name, tracks))

        elif choice in ['add']:
            new = input("Enter the playlist ID to add to the list: ")
            plists.append(new)
            name, tracks = get_playlist_details(access_token, new)
            print("Added: {} with {} songs ".format(name, tracks))

        else:
            break
