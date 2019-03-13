from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import json
from pprint import pprint
import numpy as np

# Creating our KNN Model

def scale(point):
	min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
	scaled = min_max_scaler.fit_transform(point)
	return scaled


with open("X.txt") as json_file:
	X = json.load(json_file)

with open("Y.txt") as json_file:
	y = json.load(json_file)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

X_train_data = [row[2:] for row in X_train]
X_test_data = [row[2:] for row in X_test]

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
X_train_scaled = min_max_scaler.fit_transform(X_train_data)
X_test_scaled = min_max_scaler.fit_transform(X_test_data)


knn = KNeighborsClassifier()
knn.fit(X_train_scaled, y_train)
# print(knn.predict(X_test[0:5]))
# print(knn.score(X_test, y_test))


def classify(data):
	data_scaled = scale(data)
	distances, indices = knn.kneighbors(data_scaled, n_neighbors=5)

	print(distances)
	output = [X_train[index][0:2] for index in indices[0]]
	pprint(output)


