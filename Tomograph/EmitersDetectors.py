import math


# Definicja klas
class Positions:
    def __init__(self):
        self.emiters = list()
        self.detectors = list()

    def setPositions(self, iterations, step, radius, detector_num, detector_rng):
        for i in range(0, iterations, step):
            self.emiters.append(emiterPosition(i, radius))
            self.detectors.append(detectorPosition(i, radius, detector_num, detector_rng))

        return self.emiters, self.detectors


# Definicja funkcji
def emiterPosition(angle, radius):
    x = radius * math.cos(math.radians(angle)) + radius
    y = radius * math.sin(math.radians(angle)) + radius

    return [round(x), round(y)]


def detectorPosition(angle, radius, detector_num, detector_rng):
    out = list()

    for i in range(detector_num):
        x = radius * math.cos(math.radians(angle) + math.pi - (math.radians(detector_rng) / 2)
                              + i * (math.radians(detector_rng) / (detector_num - 1)))
        y = radius * math.sin(math.radians(angle) + math.pi - (math.radians(detector_rng) / 2)
                              + i * (math.radians(detector_rng) / (detector_num - 1)))

        out.append([round(x + radius), round(y + radius)])

    return out
