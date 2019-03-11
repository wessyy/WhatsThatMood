import json

# Here's where we should analyze the data sets

# How many songs in romantic mood data set
with open('chill.txt') as json_file:
	data = json.load(json_file)
	print(len(data))