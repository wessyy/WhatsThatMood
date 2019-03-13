import os
import json
from pprint import pprint
import numpy as np
import math

# Features: lyric_sentiment and everything in "features" except type, id, uri, track_href, analysis_url

features = ['lyric_sentiment', "danceability", "energy", "loudness", "mode", "acousticness", "instrumentalness", "valence", "tempo"]
path_to_json = './data/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]


# How many songs in romantic mood data set
X = []
y = []
for file in json_files:	
	mood = file[:-4] # Strip out ".txt"
	print(mood)
	file_path = path_to_json + file
	with open(file_path) as json_file:
		data = json.load(json_file)
		for key in data:
			row = []
			if 'features' in data[key]:
				row.append(data[key]["track_name"])
				row.append(data[key]["artist_name"][0])
				if data[key]['lyric_sentiment'] == "None" or math.isnan(data[key]['lyric_sentiment']):
					row.append(0)
				else:
					row.append(data[key]['lyric_sentiment'])
				for feature in features[1:]:
					curr_feat = data[key]['features'][0][feature]
					row.append(curr_feat)

				X.append(row)
				y.append(mood)		
		

with open("X.txt", 'w') as outfile:
	json.dump(X, outfile, indent=4)

with open("Y.txt", 'w') as outfile:
	json.dump(y, outfile, indent=4)
		
		
			

	