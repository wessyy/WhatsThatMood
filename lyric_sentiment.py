import re
import numpy as np
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

#function imports
from genius_scrape import get_song_lyrics


sia = SentimentIntensityAnalyzer()
stop_words = list(stopwords.words("english"))


#returns avg sentiment of all lines
def analyze_sentiment(lyrics_arr):
	tb_sentiments = []
	nltk_sentiments = []
	for line in lyrics_arr:
		blob = TextBlob(line)
		tb_sent = blob.sentiment
		tb_sentiments.append(tb_sent.polarity)
		sia_polar =  sia.polarity_scores(line)
		# print(line)
		# print('nltk SIA: ',sia_polar, sia_polar['compound'])
		nltk_sentiments.append(sia_polar['compound'])
		# print("TextBlob sentiment: " , tb_sent)

	tb_mean = np.mean(np.array(tb_sentiments))
	nltk_mean = np.mean(np.array(np.array(nltk_sentiments)))
	# print("tb_mean: %s, nltk_mean: %s" % (tb_mean, nltk_mean))
	return tb_mean, nltk_mean

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

	# print(output_lyrics)
	
	# # return '\n'.join(output_lyrics)
	return output_lyrics

def lyric_sentiment_main(title, name):
	lyrics = get_song_lyrics(title, name)
	cleaned = clean_lyrics(lyrics)
	tb, nltks = analyze_sentiment(cleaned)
	tb1, nltks1 = analyze_sentiment(lyrics.split("\n"))
	print('tb: %s, nltks: %s' % (tb, nltks))
	print('tb1: %s, nltks1: %s' % (tb1, nltks1))

	#textblob is better.... still need to definitively choose between removing or keeping stopwords
	return tb
	



if __name__ == "__main__":
	lyric_sentiment_main("Disco Yes", "Tom Misch")
	# lyric_sentiment_main("Happy", "Pharrell Williams")



