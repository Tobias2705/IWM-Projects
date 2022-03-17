import JpgToSin
import SinToJpg
import Normalization
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from datetime import datetime
from skimage.transform import resize
from skimage.io import imread


class Tomograph:
    def __init__(self, iterations, step, detector_num, detector_rng, isFilter, isDicom, source, patient, descript):
        self.iterations = iterations
        self.step = step
        self.detector_num = detector_num
        self.detector_rng = detector_rng
        self.source = source
        self.isFilter = isFilter
        self.isDicom = isDicom

        self.img = None
        self.original = None
        self.compare = None

        self.sinograms = []
        self.reverses = []
        self.normalized = []
        self.input_image = []

        self.patient = patient
        self.descript = descript
        self.date = datetime.now()

    def main(self):
        img = cv2.cvtColor(imread(self.source), cv2.COLOR_RGBA2GRAY)
        self.original = np.copy(img)
        # Reducing photo in order to compare with out-image - MSE
        self.compare = Normalization.normalization_smaller(np.copy(img))
        # Frame_size and img_size are default equal to 1024 and 624
        self.img = Normalization.normalization(np.copy(self.original), frame_size=1024, img_size=624)

        resized = resize(self.img, (round(len(self.img) / 4), round(len(self.img[0]) / 4)))
        new_edge = round(math.sqrt(2) * max(len(resized), len(resized[0])))
        radius = round(new_edge / 2)

        self.img = np.zeros([new_edge, new_edge])
        self.img[radius - round(len(resized) / 2): radius + round(len(resized) / 2),
        radius - round(len(resized[0]) / 2): radius + round(len(resized[0]) / 2)] = resized
        self.input_image = self.img
        dims = [len(self.img), len(self.img[0])]

        # Make sinogram
        sin = JpgToSin.Sinogram()
        sin.makeSinogram(self.img, self.iterations, self.step, self.detector_num, self.detector_rng)
        self.sinograms = sin.sinograms

        # Make reverse sinogram
        rvr = SinToJpg.Reversed()
        rvr.makeReversed(sin.sinograms[-1], self.iterations, self.step, self.detector_num,
                         self.detector_rng, dims, self.input_image)
        self.reverses = rvr.reverse_sinograms

    def showImage(self, title, plot):
        fig, plots = plt.subplots(1, 2)
        plots[0].imshow(self.original, cmap='gray')
        plots[0].set_title('Obraz oryginalny')
        plots[1].imshow(plot, cmap='gray')
        plots[1].set_title(title)
