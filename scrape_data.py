import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

SPOTIPY_CLIENT_ID = '9f2764b3b60f47d88b66db6ff1f841be'
SPOTIPY_CLIENT_SECRET = 'f82c39f204834d52ac51119395703b82'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.search(q='Passion Fruit', limit=1)
song_id = results['tracks']['items'][0]['id']

features = sp.audio_features(tracks=[song_id])
pprint(features)



