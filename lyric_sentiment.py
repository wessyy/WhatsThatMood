import re
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

#function imports
from genius_scrape import get_song_lyrics


sia = SentimentIntensityAnalyzer()
stop_words = list(stopwords.words("english"))


def analyze_sentiment(lyrics_arr):
	for line in lyrics_arr:
		blob = TextBlob(line)
		tb_sent = blob.sentiment
		sia_polar =  sia.polarity_scores(line)
		print(line)
		print('nltk SIA: ',sia_polar, sia_polar['compound'])
		print("TextBlob sentiment: " , tb_sent)

def clean_lyrics(lyrics):
	repeats = 0
	output_lyrics = []
	lines_arr = lyrics.split("\n")
	# print("LENGTH OF LYRICS: " , len(lyrics_arr))
	for line in lines_arr:
		if '[' in line or ']' in line or line == '':
			continue
			continue
		elif line in lines_arr[lines_arr.index(line):]:
			#should we do something about the repeats?
			repeats += 1

		#stopwords
		line_stripped = line
		for word in stop_words:
			line_stripped = line_stripped.replace(" " + word + " ", ' ')
		output_lyrics.append(line_stripped)

	print(output_lyrics)
	
	# # return '\n'.join(output_lyrics)
	return output_lyrics



if __name__ == "__main__":
	lyrics = get_song_lyrics("Happy", "Pharrell Williams")
	# analyze_sentiment(lyrics)
	cleaned = clean_lyrics(lyrics)
	analyze_sentiment(cleaned)