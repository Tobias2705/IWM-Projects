from keras import models

import Effectiveness
import Image as Img
import Effectiveness as EF
import numpy as np
from matplotlib import pylab as plt
import Processing
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import Flatten
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.utils.np_utils import to_categorical

# Global variables
sampleSizeV = 5
samplingPercentageV = 0.2


def countMetrics(data, pred):
    positive_all = 0
    negative_all = 0
    positive_true = 0
    negative_true = 0
    positive_false = 0
    negative_false = 0

    for i in range(len(pred)):
        if data[i][0] > data[i][1]:
            positive_all += 1
            if pred[i][0] > pred[i][1]:
                positive_true += 1
            else:
                positive_false += 1
        else:
            negative_all += 1
            if pred[i][0] < pred[i][1]:
                negative_true += 1
            else:
                negative_false += 1
    print(">>")
    #Effectiveness.checkEffectiveness2(positive_true, positive_false, negative_false, negative_true)
    acc = (positive_true + negative_true) / (positive_all + negative_all)

    sen = positive_true / (positive_true + negative_false)
    spec = negative_true / (negative_true + positive_false)

    neg = negative_true / (negative_true + negative_false)
    prec = positive_true / (positive_true + positive_false)

    return acc, sen, spec, neg, prec


class MachineLearning:
    def __init__(self):
        self.datasetX = []
        self.datasetY = []
        # Model
        self.model = None

    def __getImageValuesAsModelData(self, img, hoImg, size, percentage):
        sampleSize = size
        samplingPercentage = percentage
        dataX = []
        dataY = []

        for x in range(len(img)):
            height, width, depth = img[x].shape

            for i in range(0, height - sampleSize):
                for j in np.floor(np.arange(0, width - sampleSize, 1 / samplingPercentage)).astype(int):
                    arr_sample = img[x][i: i + sampleSize, j: j + sampleSize]
                    dataX.append(np.array(arr_sample))

                    arr_ground_sample = hoImg[x][i: i + sampleSize, j: j + sampleSize]
                    #print(arr_sample)
                    #print(arr_ground_sample)
                    point_y = arr_ground_sample[sampleSize // 2][sampleSize // 2]
                    #print(point_y)
                    point_mean = np.mean(point_y)

                    if point_mean > 50:
                        dataY.append(1)
                    else:
                        dataY.append(0)

        self.datasetX = np.array(dataX)
        self.datasetY = to_categorical(dataY)

    def createModel(self):
        self.model = Sequential()

        self.model.add(Conv2D(70, kernel_size=3, activation='relu', input_shape=(5, 5, 3)))
        self.model.add(Conv2D(45, kernel_size=3, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(2, activation='softmax'))

        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def testData(self, paths, hoPaths):
        img = []
        hoImg = []
        for i in range(18):
            img.append(Img.loadImageML(paths[i]))
            hoImg.append(Img.loadImageML(hoPaths[i]))
        self.__getImageValuesAsModelData(img, hoImg, sampleSizeV, samplingPercentageV)

    def trainModel(self):
        train_data, test_data, train_labels, test_labels = train_test_split(self.datasetX,
                                                                            self.datasetY,
                                                                            test_size=0.25,
                                                                            random_state=42)
        self.model.fit(train_data, train_labels, validation_data=(test_data, test_labels), epochs=150)
        self.model.save("model_v250.h5")

    def anotherImagesResult(self, paths, hoPaths):

        avg_accuracy = avg_sensitivity = avg_specificity = avg_negative = avg_precision = s = 0
        model = models.load_model("model_v250.h5")
        for k in range(0, 5):
            img = Img.loadImageML(paths[k + 18])
            ground_truth = Img.loadImageML(hoPaths[k + 18])

            self.__getImageValuesAsModelData([img], [ground_truth], sampleSizeV, 1)
            prediction = model.predict(self.datasetX)

            height, width, depth = img.shape

            comparsion = []
            pixel_img = []

            for i in range(0, height - sampleSizeV):
                row_comparsion = []
                row_pixel = []
                for j in range(0, width - sampleSizeV):

                    index = (width - sampleSizeV) * i + j
                    #(index,  prediction[index])
                    point = np.mean(ground_truth[i][j])

                    isVessel = False
                    if point > 50.0:
                        isVessel = True

                    if prediction[index][0] < prediction[index][1]:
                        row_pixel.append(1)

                        if isVessel:
                            row_comparsion.append(np.array([255, 255, 255]))
                        else:
                            row_comparsion.append(np.array([255, 0, 0]))
                    else:
                        row_pixel.append(0)

                        if not isVessel:
                            row_comparsion.append(np.array([0, 0, 0]))
                        else:
                            row_comparsion.append(np.array([0, 255, 0]))

                comparsion.append(np.array(row_comparsion))
                pixel_img.append(np.array(row_pixel))

            acc, sen, spec, neg, prec = countMetrics(self.datasetY, prediction)
            #print("=============")
            hold = (Processing.preProcessing( ground_truth, [0]) / 255).astype(int)
            #print(type(pixel_img), hold.shape, pixel_img[120], hold[120])

            avg_accuracy += acc
            avg_sensitivity += sen
            avg_specificity += spec
            avg_negative += neg
            avg_precision += prec

            print("--------" + " Wyniki dla zbioru nr " + str(k) + " --------")
            print("Accuracy: " + str(acc))

            print("Sensitivity: " + str(sen))
            print("Specificity: " + str(spec))

            print("Negative predictive value: " + str(neg))
            print("Precision: " + str(prec))

            comparsion = np.array(comparsion)
            pixel_img = np.array(pixel_img)
            print(k)
            plt.figure(figsize=(20, 10))

            plt.subplot(1, 4, 1)
            plt.axis('off')
            plt.imshow(img)
            plt.title('original')

            plt.subplot(1, 4, 2)
            plt.axis('off')
            plt.imshow(comparsion)
            plt.title('comparsion')

            plt.subplot(1, 4, 3)
            plt.axis('off')
            plt.imshow(pixel_img, cmap="gray")
            plt.title('predicted')

            plt.subplot(1, 4, 4)
            plt.axis('off')
            plt.imshow(ground_truth)
            plt.title('Ground_truth')
            s += 1
        
        print("Ogólne rezultaty")
        print("Średnie wyniki dla tego rozwiązania")
        print("średnie accuracy: " + str(avg_accuracy / s))
        print("średnie sensitivity: " + str(avg_sensitivity / s))
        print("średnie specificity: " + str(avg_specificity / s))
        print("średnie negative predictive value: " + str(avg_negative / s))
        print("średnie precision: " + str(avg_precision / s))
