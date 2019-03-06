import lyricsgenius


GENIUS_CLIENT_ID = 'nGsCM36owuwGUH_9gSGRuJinaxMb8JuINkgigUz2uPTuu4zBR1k5R6NHC1eRuGia'
GENIUS_CLIENT_ID_SECRET = 'Jf5ByTVljrgDlPmjYn2e0zLx41uM24bpjxIcEA3aC0D98ibXgmLd98PQPVazNd6QP5dUzNS0iFag6bf_L-UPYw'
GENIUS_CLIENT_ACCESS_TOKEN = 'Zm_qKkcc6rTH16SzZpJCJu_qTYgniy7XxqDS0KcOBltEddWAm4bwcxAOFwkOYO8o'
genius = lyricsgenius.Genius(GENIUS_CLIENT_ACCESS_TOKEN)

def get_song_lyrics(title, person):
	# artist = genius.search_artist(person, max_songs=1)
	song = genius.search_song(title, person)
	print(song.lyrics)
	return song.lyrics


if __name__ == "__main__":
	get_song_lyrics("Anita", "Smino")
