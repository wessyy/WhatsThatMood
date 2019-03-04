import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from musixmatch import Musixmatch
from pprint import pprint
import requests
import json

SPOTIPY_CLIENT_ID = '9f2764b3b60f47d88b66db6ff1f841be'
SPOTIPY_CLIENT_SECRET = 'f82c39f204834d52ac51119395703b82'

MUSIXMATCH_CLIENT_ID = 'f5a52968523f560cc30234c38bf644ab'

GENIUS_CLIENT_ID = 'nGsCM36owuwGUH_9gSGRuJinaxMb8JuINkgigUz2uPTuu4zBR1k5R6NHC1eRuGia'
GENIUS_CLIENT_ID_SECRET = 'Jf5ByTVljrgDlPmjYn2e0zLx41uM24bpjxIcEA3aC0D98ibXgmLd98PQPVazNd6QP5dUzNS0iFag6bf_L-UPYw'
GENIUS_CLIENT_ACCESS_TOKEN = 'Zm_qKkcc6rTH16SzZpJCJu_qTYgniy7XxqDS0KcOBltEddWAm4bwcxAOFwkOYO8o'

# website url: https://kimberlykwon.github.io/WhatsThatMoodSite/

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
access_token = client_credentials_manager.get_access_token()
auth_string = "Bearer " + access_token

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
mm = Musixmatch(MUSIXMATCH_CLIENT_ID)

# # SEARCHING FOR STUFF EXAMPLE
# results = sp.search(q='Passion Fruit', limit=1)
# song_id = results['tracks']['items'][0]['id']

# features = sp.audio_features(tracks=[song_id])

categories = sp.categories()
category_ids = [c['id'] for c in categories['categories']['items']]

# TODO: Aggregate data into json file. RN just parsing through to see what we get
# Loop through all categories
for category in category_ids:
	# Get first playlist from category and then get the tracks on it
	category_playlists = sp.category_playlists(category_id=category, limit=1)
	endpoint = category_playlists['playlists']['items'][0]['tracks']['href']

	response = requests.get(endpoint, headers={"Authorization": auth_string})
	tracks = response.json()

	# Analyze tracks for audio features
	for item in tracks['items']:
		print("********** NEW TRACK ALERT *****************")
		data = {}
		data['track_id'] = item['track']['id']
		data['track_name'] = item['track']['name']
		data['artist_id'] = [artist['id'] for artist in item['track']['artists']]
		data['artist_name'] = [artist['name'] for artist in item['track']['artists']]
		print (data['track_name'])
		tracks_results = mm.track_search(q_track = item['track']['name'], q_artist = data['artist_name'][0], page_size = 1, page = 1, s_track_rating = 'desc')['message']['body']['track_list'] # check
		mm_track_id = tracks_results[0]['track']['track_id']
		mm_lyrics_result = mm.track_lyrics_get(mm_track_id)['message']['body']['lyrics']['lyrics_body']
		# data['partial_lyrics'] = mm.track_lyrics_get(mm_track_id) #check
		print (mm_lyrics_result)
		
		track_id = item['track']['id']
		# track_name = item['track']['name']
		# artist_id = [artist['id'] for artist in item['track']['artists']]
		# artist_name = [artist['name'] for artist in item['track']['artists']]

		# track = sp.track(track_id)
		features = sp.audio_features(tracks = track_id)
		analysis = sp.audio_analysis(track_id)  # Gives a whole bunch of shit


		# merged = {**features[0], **analysis[0]}

		# pprint(data)
		# pprint(merged)


		# pprint(track)
		# pprint(features)

		break
	
	break
	


