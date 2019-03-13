import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
from pprint import pprint
import requests
import json
from lyric_sentiment import get_sentiment
import math
from classifier import classify


SPOTIPY_CLIENT_ID = '9f2764b3b60f47d88b66db6ff1f841be'
SPOTIPY_CLIENT_SECRET = 'f82c39f204834d52ac51119395703b82'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
access_token = client_credentials_manager.get_access_token()
auth_string = "Bearer " + access_token
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def analyze_features(artist, song):
	search_string = "artist:" + artist + " track:" + song
	search_query = sp.search(q=search_string, type='track', limit=1)


	features = ['lyric_sentiment', "danceability", "energy", "loudness", "mode", "acousticness", "instrumentalness", "valence", "tempo"]
	data = []

	audio_features = sp.audio_features(tracks = search_query['tracks']['items'][0]['id'])
	lyrics_sentiment = get_sentiment(song, artist)
	if lyrics_sentiment == "None" or math.isnan(lyrics_sentiment):
		data.append(0)
	else:
		data.append(lyrics_sentiment)
	for feature in features[1:]:
		data.append(audio_features[0][feature])

	return data



if __name__ == '__main__':
	# Enter artist and song you want to check
	artist = "Daddy Yankee"
	song = "Limbo"
	features = analyze_features(artist, song)
	classify([features])


