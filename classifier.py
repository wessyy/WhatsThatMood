from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
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
	return [row[1:] for row in X]

# def test():
# 	X, y = generate_X_and_Y()
# 	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

# 	# Take out song and artist
# 	X_train_data = strip_song_and_artist(X_train)
# 	X_test_data = strip_song_and_artist(X_test)

# 	# Scale
# 	X_train_scaled = preprocessing.scale(X_train_data)
# 	X_test_scaled = preprocessing.scale(X_test_data)

# 	knn = KNeighborsClassifier(n_neighbors=20, weights='distance', algorithm='brute')
# 	knn.fit(X_train_scaled, y_train)
# 	print(knn.score(X_test_scaled, y_test))
	
# 	# # Using cross validation look at accuracy
# 	# X_data = [row[2:] for row in X]
# 	# cv_scores = cross_val_score(knn, X_data, y, cv=5)
# 	# print(cv_scores)
# 	# print("cv_scores mean:{}".format(np.mean(cv_scores)))


def score():
	X, y = generate_X_and_Y()
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

	# Take out song and artist
	X_train_data = strip_song_and_artist(X_train)
	X_test_data = strip_song_and_artist(X_test)

	# Scale
	X_train_scaled = preprocessing.scale(X_train_data)
	X_test_scaled = preprocessing.scale(X_test_data)

	# fit our model
	knn = KNeighborsClassifier(n_neighbors=20, weights='distance', algorithm='brute')
	knn.fit(X_train_scaled, y_train)

	correct = 0
	total = 0
	with open('overlap.txt', 'r') as json_file:
		overlap_data = json.load(json_file)
		for i in range(0, len(X_test_scaled)):
			prediction = knn.predict([X_test_scaled[i]])
			# print("prediction: ", prediction)
			# print(overlap_data[X_test[i][0]])
			if prediction in overlap_data[X_test[i][0]]:
				correct += 1
			total += 1


	print(correct/total)
	return correct/total





def classify(data):
	X, y = generate_X_and_Y()
	X_data = strip_song_and_artist(X)
	X_scaled = scale(X_data)

	knn = KNeighborsClassifier(n_neighbors=20)
	knn.fit(X_data, y)

	data_scaled = scale(data)
	print("Predicted Mood:", knn.predict(data))
	print("accuracy:", knn.score(X_data, y))
	distances, indices = knn.kneighbors(data, n_neighbors=20)

	# Moods + songs & artists of K nearest neighbors
	moods = [y[index] for index in indices[0]]
	songs_and_artists = [X[index][0:2] for index in indices[0]]
	sa_classes = [y[index] for index in indices[0]]
	# print("moods:")
	# pprint(moods)
	# print("indices:")
	# pprint(indices)
	for i in range(0, len(songs_and_artists)):
		print(songs_and_artists[i])
		print(sa_classes[i])
	# print("songs and artists:")
	# pprint(songs_and_artists)
	# print("their moods:")
	# pprint(sa_classes)

	return moods




if __name__ == '__main__':
	score()






