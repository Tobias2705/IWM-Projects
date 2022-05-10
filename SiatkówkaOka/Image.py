import Processing
import cv2
from matplotlib import pyplot as plt


def loadImage(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def loadImageML(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def getPreparedImage(img):
    preparedImage = Processing.preProcessing(img, [0, 1, 7, 5, 9])
    preparedImage = Processing.lighten(preparedImage)
    return preparedImage


def getResultImage(img):
    resultImage = Processing.properProcessing(img)
    resultImage = Processing.preProcessing(resultImage, [1, 8, 3])
    return resultImage


def getResultBinary(img, prepImg):
    resultBinary = Processing.preProcessing(img > 30, [6]).astype(int)
    resultBinary = Processing.removeBorder(prepImg, resultBinary)
    return resultBinary


def getHoldOut(path):
    holdOut = (Processing.preProcessing(loadImage(path), [0]) / 255).astype(int)
    return holdOut


class Image:
    def __init__(self):
        self.original = None
        self.prepared = None
        self.result = None
        self.binary = None
        self.holdOut = None
        self.outPut = None
        self.images = []

    def imageProcess(self, path, holdPath):
        self.original = loadImage(path)
        self.prepared = getPreparedImage(self.original)
        self.result = getResultImage(self.prepared)
        self.binary = getResultBinary(self.result, self.prepared)
        self.holdOut = getHoldOut(holdPath)
        self.outPut = Processing.applyBinary(self.binary, self.original)

    def showImages(self):
        plt.figure(figsize=(15, 20))
        plt.subplot(3, 2, 1)
        plt.imshow(self.original, cmap='gray')
        plt.axis('off')
        plt.title('Original')

        plt.subplot(3, 2, 2)
        plt.imshow(self.prepared, cmap='gray')
        plt.axis('off')
        plt.title('Prepared')

        plt.subplot(3, 2, 3)
        plt.imshow(self.binary, cmap='gray')
        plt.axis('off')
        plt.title('Binary')

        plt.subplot(3, 2, 4)
        plt.imshow(self.holdOut, cmap='gray')
        plt.axis('off')
        plt.title('Hold Out')

        plt.subplot(3, 2, 5)
        plt.imshow(self.original, cmap='gray')
        plt.axis('off')
        plt.title('Original')

        plt.subplot(3, 2, 6)
        plt.imshow(self.outPut, cmap='gray')
        plt.axis('off')
        plt.title('Visualization')
