import os
import json
from pprint import pprint



def find_all_moods_all_songs():
	moods_dict = {}

	path_to_json = './data/'
	json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]
	for file in json_files:
		mood = file[:-4]
		file_path = path_to_json + file
		with open(file_path) as json_file:
			data = json.load(json_file)
			for songdata in data:
				if songdata in moods_dict:
					moods_dict[songdata].append(mood)
				else:
					moods_dict[songdata] = [mood]

	# pprint(moods_dict)
	with open("overlap.txt", 'w') as outfile:
		json.dump(moods_dict, outfile, indent=4)
	return moods_dict

def find_overlap(mood1, mood2):
	moods_dict = find_all_moods_all_songs()
	mood1_songs = 0
	mood2_songs = 0
	overlap = 0
	for song in moods_dict:
		song_moods = moods_dict[song]
		# print(song)
		# print(song_moods)
		if mood1 in song_moods and mood2 in song_moods:
			overlap += 1
		if mood1 in song_moods:
			mood1_songs += 1
		if mood2 in song_moods:
			mood2_songs += 1
	# print(overlap, mood1_songs, mood2_songs)
	return overlap / mood1_songs, overlap / mood2_songs







if __name__ == "__main__":
	# moods = ['romantic', 'happy', 'sad', 'chill', 'angry', 'peaceful', 'energizing', 'upbeat', 'sensual']

	path_to_json = './data/'
	moods = [pos_json[:-4] for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]

	overlaps = {}
	for i in range(0, len(moods)-1):
		for j in range(i+1, len(moods)):
			key = moods[i] + ' ' + moods[j]
			overlaps[key] = find_overlap(moods[i], moods[j])
	# print(find_overlap('upbeat', 'happy'))
	# pprint(overlaps)






