import Bresenham
import EmitersDetectors
import numpy as np


# Definicja klas
class Sinogram:
    def __init__(self):
        self.sinograms = []

    def makeSinogram(self, img, iterations, step, detector_num, detector_rng):
        pos = EmitersDetectors.Positions()
        radius = round(len(img) / 2) - 1

        emiters, detectors = pos.setPositions(iterations, step, radius, detector_num, detector_rng)
        sinogram = np.zeros([len(emiters), len(detectors[0])])

        for i, [eX, eY] in enumerate(emiters):
            for j, [dX, dY] in enumerate(detectors[i]):
                line = Bresenham.BresenhamLine(eX, eY, dX, dY)

                for x, y in line:
                    sinogram[i, j] += img[x, y]
            self.sinograms.append(np.copy(sinogram))
