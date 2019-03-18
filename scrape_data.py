import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
from pprint import pprint
import requests
import json
from lyric_sentiment import get_sentiment

SPOTIPY_CLIENT_ID = '9f2764b3b60f47d88b66db6ff1f841be'
SPOTIPY_CLIENT_SECRET = 'f82c39f204834d52ac51119395703b82'

GENIUS_CLIENT_ID = 'nGsCM36owuwGUH_9gSGRuJinaxMb8JuINkgigUz2uPTuu4zBR1k5R6NHC1eRuGia'
GENIUS_CLIENT_ID_SECRET = 'Jf5ByTVljrgDlPmjYn2e0zLx41uM24bpjxIcEA3aC0D98ibXgmLd98PQPVazNd6QP5dUzNS0iFag6bf_L-UPYw'
GENIUS_CLIENT_ACCESS_TOKEN = 'Zm_qKkcc6rTH16SzZpJCJu_qTYgniy7XxqDS0KcOBltEddWAm4bwcxAOFwkOYO8o'
genius = lyricsgenius.Genius(GENIUS_CLIENT_ACCESS_TOKEN)

# website url: https://kimberlykwon.github.io/WhatsThatMoodSite/

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
access_token = client_credentials_manager.get_access_token()
auth_string = "Bearer " + access_token

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

categories = sp.categories()
category_ids = [c['id'] for c in categories['categories']['items']]


def scrape_data(mood):
	output_file = mood + ".txt"
	playlist_results = sp.search(q = mood, type = 'playlist', limit = 20)
	playlist_items = playlist_results['playlists']['items']

	tracks_by_mood = {}
	for item in playlist_items:
		print("Analyzing songs from:", item['name'])
		endpoint = item['tracks']['href']

		response = requests.get(endpoint, headers={"Authorization": auth_string})
		tracks = response.json()
		try:
			for item in tracks['items']:
				data = {}
				try:
					data['track_id'] = item['track']['id']
					data['track_name'] = item['track']['name']
					data['artist_id'] = [artist['id'] for artist in item['track']['artists']]
					data['artist_name'] = [artist['name'] for artist in item['track']['artists']]

					lyrics_sentiment = get_sentiment(data['track_name'], data['artist_name'][0])
					# print("searching song %s by %s" % (data['track_name'], data['artist_name'][0]))
					data['lyric_sentiment'] = lyrics_sentiment
					
					if data['track_id']:
						features = sp.audio_features(tracks = data['track_id'])
						data['features'] = features		

					key = ' '.join([data['track_name'], ' '.join(data['artist_name'])])
					# print(key)
					tracks_by_mood[key] = data # set key to id so we don't get repeats
					with open(output_file, 'w') as outfile:
						json.dump(tracks_by_mood, outfile, indent=4) 	
				except:
					continue
		except:
			continue
	print("Done")


		

if __name__ == "__main__":
	moods = ['romantic', 'happy', 'sad', 'chill', 'angry', 'peaceful', 'energizing', 'upbeat', 'sensual'] # change
	mood = 'sensual'
	scrape_data(mood)


