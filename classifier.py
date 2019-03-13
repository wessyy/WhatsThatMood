from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
import json
from pprint import pprint
import numpy as np

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# Creating our KNN Model

def scale(point):
	min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
	scaled = min_max_scaler.fit_transform(point)
	return scaled


def generate_X_and_Y():
	with open("X.txt") as json_file:
		X = json.load(json_file)

	with open("Y.txt") as json_file:
		y = json.load(json_file)

	X = np.array(X)
	y = np.array(y)

	return X, y

def strip_song_and_artist(X):
	return [row[2:] for row in X]


def test():
	X, y = generate_X_and_Y()
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

	# Take out song and artist
	X_train_data = strip_song_and_artist(X_train)
	X_test_data = strip_song_and_artist(X_test)

	# Scale
	X_train_scaled = scale(X_train_data)
	X_test_scaled = scale(X_test_data)

	knn = KNeighborsClassifier(n_neighbors=5)
	knn.fit(X_train_scaled, y_train)
	print(knn.score(X_test_scaled, y_test))
	
	# # Using cross validation look at accuracy
	# X_data = [row[2:] for row in X]
	# cv_scores = cross_val_score(knn, X_data, y, cv=5)
	# print(cv_scores)
	# print("cv_scores mean:{}".format(np.mean(cv_scores)))


def classify(data):
	X, y = generate_X_and_Y()
	X_data = strip_song_and_artist(X)
	X_scaled = scale(X_data)
	
	knn = KNeighborsClassifier(n_neighbors=5)
	knn.fit(X_scaled, y)

	data_scaled = scale(data)
	print("Predicted Mood:", knn.predict(data_scaled))
	distances, indices = knn.kneighbors(data_scaled, n_neighbors=5)

	# Moods + songs & artists of K nearest neighbors
	moods = [y[index] for index in indices[0]]
	songs_and_artists = [X[index][0:2] for index in indices[0]]
	pprint(moods)
	pprint(songs_and_artists)


if __name__ == '__main__':
	test()