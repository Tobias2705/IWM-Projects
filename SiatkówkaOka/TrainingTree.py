from matplotlib import pyplot as plt

import SegmentAnalysis as SA
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, cross_validate, KFold
import numpy as np

np.seterr(divide='ignore', invalid='ignore')


class Classifier:
    def __init__(self, preparedImage, holdout):
        self.data, self.target = SA.prepareData(preparedImage, holdout)
        self.decisionTree = DecisionTreeClassifier(criterion='entropy')
        self.accuracy_model = []
        self.data_test = None
        self.target_test = None
        self.predicted = None

    def training(self):
        for train_index, test_index in KFold(n_splits=5, shuffle=False).split(self.data):
            X_train, X_test = list(map(self.data.__getitem__, train_index)), list(
                map(self.data.__getitem__, test_index))
            y_train, y_test = list(map(self.target.__getitem__, train_index)), list(
                map(self.target.__getitem__, test_index))

            model = self.decisionTree.fit(X_train, y_train)
            self.accuracy_model.append(round(accuracy_score(y_test, model.predict(X_test), normalize=True) * 100, 3))

        print('Accuracy score: {}'.format(self.accuracy_model))
        print('Cross-validated score: {}'.format(np.round(cross_val_score(model, self.data, self.target) * 100, 3)))
        print('Score: {}'.format(round(self.decisionTree.score(X_test, y_test) * 100, 3)))
        print('')

    def predicting(self):
        self.decisionTree.fit(self.data, self.target)
        self.predicted = self.decisionTree.predict(self.data_test)

    def testing(self, preparedtest, holdoutTest):
        self.training()
        self.data_test, self.target_test = SA.prepareData(preparedtest, holdoutTest)
        self.predicting()

    def show3(self, prepared):
        fig = plt.figure(figsize=(15, 20))
        plt.subplot(1, 3, 1)
        plt.imshow(prepared, cmap='gray')
        plt.axis('off')
        plt.title('Test image')

        plt.subplot(1, 3, 2)
        plt.imshow(self.predicted.reshape(192, 200), cmap='gray')
        plt.axis('off')
        plt.title('Predicted')

        plt.subplot(1, 3, 3)
        plt.imshow(self.target_test.reshape(192, 200), cmap='gray')
        plt.axis('off')
        plt.title('HoldOut')
