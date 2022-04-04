import cv2
import numpy as np
from skimage import img_as_ubyte, exposure
from skimage.filters import unsharp_mask, sato


def preProcessing(img, optionNumbers):
    for num in optionNumbers:
        if num == 0:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        elif num == 1:
            img = img_as_ubyte(unsharp_mask(img, radius=5, amount=2))

        elif num == 2:
            kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            img = cv2.filter2D(img, -1, kernel_sharpening)

        elif num == 3:
            img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        elif num == 4:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            img = clahe.apply(img)

        elif num == 5:
            invGamma = 0.75
            table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
            img = cv2.LUT(img, table)

        elif num == 6:
            nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(np.uint8(img), connectivity=8)
            sizes = stats[1:, -1]
            nb_components = nb_components - 1
            min_size = 600
            img = np.zeros(output.shape)
            for i in range(0, nb_components):
                if sizes[i] >= min_size:
                    img[output == i + 1] = 1

        elif num == 7:
            img = img_as_ubyte(exposure.equalize_adapthist(img, clip_limit=0.01))

        elif num == 8:
            img = cv2.dilate(img, np.ones((1, 1), np.uint8), iterations=1)

        elif num == 9:
            img = cv2.erode(img, np.ones((2, 2), np.uint8), iterations=1)

    return img


def properProcessing(img):
    img = sato(img, mode='constant')
    return img_as_ubyte(img)


def removeBorder(original, img):
    for i in range(len(original)):
        for j in range(len(original[0])):
            if original[i][j] < 50:
                img[i][j] = 0
    return img


def lighten(img):
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] > 75:
                if img[i][j] <= 250:
                    img[i][j] += 5
            else:
                if img[i][j] < 76:
                    if img[i][j] > 5:
                        img[i][j] -= 5

    return img


def applyBinary(binar, org):
    ori = np.copy(org)
    for i in range(len(binar)):
        for j in range(len(binar[0])):
            if binar[i][j] > 0:
                ori[i][j] = 255

    return ori
