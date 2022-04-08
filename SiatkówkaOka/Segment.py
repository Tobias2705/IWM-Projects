
from math import ceil
from skimage.measure import moments_central, moments_hu
from skimage.util import img_as_float
from statistics import variance

class Segment:
    def __init__(self, img, holdOut):
        self.img = img_as_float(img)
        self.colorVariance = variance(self.img.flatten())
        self.centralMoments = moments_central(self.img)
        self.huMoments = moments_hu(self.img)
        self.isVesselBin = holdOut[ceil(len(holdOut) / 2)][ceil(len(holdOut) / 2)]
    def __repr__(self):
        return str([self.colorVariance]) + "\n" + str(self.centralMoments.flatten()) + "\n" + str(self.huMoments) + "\n" + str(self.isVesselBin)

    def getData(self):
        return [*[self.colorVariance], *self.centralMoments.flatten(), *self.huMoments]