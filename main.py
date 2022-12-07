import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "0f5ff4e3d7534cb79e2a24157d10db68"
CLIENT_SECRET = "8078e185385c49d49bf4d1649ec4fec5"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

scope = "playlist-modify-private"
spotify_auth = spotipy.oauth2.SpotifyOAuth(
    scope=scope,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    show_dialog=True,
    cache_path="token.txt"
    )

sp = spotipy.Spotify(oauth_manager=spotify_auth)
USER_ID = sp.current_user()['id']
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all(name="h3", class_="a-no-trucate", id="title-of-a-story")

song_uris = []
year = date.split("-")[0]

song_list = [song.getText().strip("\n\t") for song in songs]

for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=USER_ID, name=f"{date} Billboard 100", public=False, description="Music Time Machine")
playlist_id = playlist['id']

sp.playlist_add_items(playlist_id, items=song_uris)

