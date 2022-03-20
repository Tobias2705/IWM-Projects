import Bresenham
import EmitersDetectors
import numpy as np

# Definicja klas
class Reversed:
    def __init__(self):
        self.reverse_sinograms = []

    def makeReversed(self, img, iterations, step, detector_num, detector_rng, dimensions, input_img):
        pos = EmitersDetectors.Positions()
        radius = round(len(input_img) / 2) - 1

        emiters, detectors = pos.setPositions(iterations, step, radius, detector_num, detector_rng)
        reverse_sinogram = np.zeros(dimensions)

        for i, [eX, eY] in enumerate(emiters):
            for j, [dX, dY] in enumerate(detectors[i]):
                line = Bresenham.BresenhamLine(eX, eY, dX, dY)
                for x, y in line:
                    reverse_sinogram[x, y] += img[i, j]
            reverse = reverse_sinogram[round(len(input_img) / 4): 3 * round(len(input_img) / 4),
                      round(len(input_img[0]) / 4): 3 * round(len(input_img[0]) / 4)]
            self.reverse_sinograms.append(np.copy(reverse))