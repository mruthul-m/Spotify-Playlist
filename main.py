import requests
from datetime import datetime
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET = "YOUR CLINT SECRET"

REDIRECT_URI = "YOU CAN CREATE A URI TO GENERATE A TOKEN eg: https://example.com/"

# scope means as permissions
SCOPE = "playlist-read-private playlist-modify-private"

# you get the permission request, grant it.

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI,
        show_dialog=True,
        cache_path="token.txt",
    )
)


user_id = sp.current_user()["id"]

# Now You can create your own playlist
NAME = "My-PlayList"
DESCRIPTION = "GIVE THE DESCRIPTION FOR YOUR PLAYLIST"

playlist = sp.user_playlist_create(
    user=user_id,
    name=NAME,
    public=True,
    collaborative=False,
    description=DESCRIPTION,
)

playlsit_id = playlist["id"]

format = "%Y-%m-%d"


start = True
while start:
    input("We are Collecting music from the billboard site for the most played 100songs.")
    user_date = input("Please enter your preffered Date in the format YYYY-MM_DD: ")
    try:
        bool(datetime.strptime(user_date, format))
    except ValueError:
        print("Your format of the date is invalid")
    else:
        start = False
        year = user_date.split("-")[0]
        billboard_url = f"https://www.billboard.com/charts/hot-100/{user_date}/"
        response = requests.get(url=billboard_url)
        soup = BeautifulSoup(response.text, "html.parser")
        song_uris = []
        songs = soup.select(selector="li #title-of-a-story")
        for song in songs:
            track = song.get_text().strip()
            song_spotify = sp.search(q=f"track:{track} year:{year}", type="track")
            try:
                uri = song_spotify["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                print(f"{track} doesn't exist on spotify")

sp.playlist_add_items(playlist_id=playlsit_id, items=song_uris, position=None)

print(f"Your Playlist is ready: https://open.spotify.com/playlist/{playlsit_id}")
