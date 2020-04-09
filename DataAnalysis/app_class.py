# import the necessary packages
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.datasets import load_iris
import pandas as pd
import argparse
import xlrd
import numpy as np
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", type=str, default="mlp", help="type of python machine learning model to use")
args = vars(ap.parse_args())

# define the dictionary of models our script can use, where the key
# to the dictionary is the name of the model (supplied via command
# line argument) and the value is the model itself
models = {"knn": KNeighborsClassifier(n_neighbors=1),
          "naive_bayes": GaussianNB(),
          "logit": LogisticRegression(solver="lbfgs", multi_class="auto"),
          "svm": SVC(kernel="rbf", gamma="auto"),
          "decision_tree": DecisionTreeClassifier(),
          "random_forest": RandomForestClassifier(n_estimators=100),
          "mlp": MLPClassifier()}

# load the Iris dataset and perform a training and testing split,
# using 75% of the data for training and 25% for evaluation
print("[INFO] loading data...")
file_location = r'C:\Users\Lucypoo\Documents\MachineLearning\AIPacMan\PyProject\pacman.xlsx'
data_set = pd.read_excel(r'C:\Users\Lucypoo\Documents\MachineLearning\AIPacMan\PyProject\pacman.xlsx')
workbook = xlrd.open_workbook(file_location)
data_set_target = pd.DataFrame(data_set, columns=['PLAYER DIRECTION'])
data_set_data = pd.DataFrame(data_set, columns=['-2,-2', '-1,-2', '0, -2', '1, -2', '2, -2', '-2, -1', '-1, -1',
                                                '0, -1', '1, -1', '2, -1', '-2, 0', '-1, 0', '1, 0', '2, 0', '-2, 1',
                                                '-1, 1', '0, 1', '1, 1', '2, 1', '-2, 2', '-1, 2', '0, 2', '1, 2',
                                                '2, 2']).fillna(999)
(trainX, testX, trainY, testY) = train_test_split(data_set_data, data_set_target, test_size=0.25,  random_state=3)

# train the model
print("[INFO] using '{}' model".format(args["model"]))
model = models[args["model"]]
#print(data_set_data)
model.fit(trainX, trainY)

# make predictions on our data and show a classification report
print("[INFO] evaluating...")
predictions = model.predict(testX)
print(classification_report(testY, predictions,))
