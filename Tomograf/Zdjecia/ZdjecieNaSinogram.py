import Bresenham
import numpy as np


# Definicja klas
class Sinogram:
    def __init__(self):
        self.sin = []
        self.linie = []


class Pixel:
    def __init__(self):
        self.max = int(0)
        self.znormalizowany = np.float(0)
        self.czysty = np.float(0)

    def wartosc(self, zdj, linia):
        for p in linia:
            if 0 <= p[0] < len(zdj) and 0 <= p[1] < len(zdj):
                self.czysty += float(zdj[int(p[0]), int(p[1])])
                self.max += 1
        if self.max != 0:
            self.znormalizowany = self.czysty / self.max


def zdjNAsinogram(zdj, **kwargs):
    sinogram = Sinogram()

    # Definicja parametrów
    parametry = {
        'krok': 2,
        'liczba_detektorow': 360,
        'rozwartosc': 90
    }

    # Ewentualna zmiana parametrów przez użytkownika
    parametry.update(kwargs)

    krok = parametry['krok']
    liczba = parametry['liczba_detektorow']
    rozwartosc = parametry['rozwartosc']

    rozmiarZdj = len(zdj[0])
    promien = int(np.ceil(np.sqrt(rozmiarZdj * rozmiarZdj)))

    # Główna pętla odpowiedzialna za proszuanie emiterem
    for i in range(0, 360, krok):
        sinogram.sin.append([])
        sinogram.linie.append([])

        for detector in range(0, liczba):
            x1 = promien * np.cos(i * np.pi / 180)
            y1 = promien * np.sin(i * np.pi / 180)

            x2 = promien * np.cos((i + 180 - (rozwartosc / 2) + detector * (rozwartosc / (liczba - 1))) * np.pi / 180)
            y2 = promien * np.sin((i + 180 - (rozwartosc / 2) + detector * (rozwartosc / (liczba - 1))) * np.pi / 180)

            x1 += np.floor(rozmiarZdj / 2)
            x2 += np.floor(rozmiarZdj / 2)
            y1 += np.floor(rozmiarZdj / 2)
            y2 += np.floor(rozmiarZdj / 2)

            linia = Bresenham.BresenhamLine(x1, y1, x2, y2)

            pixel = Pixel()
            pixel.wartosc(zdj, linia)

            sinogram.sin[-1].append(pixel.znormalizowany)
            sinogram.linie[-1].append([x1, y1, x2, y2])

    return sinogram.sin, sinogram.linie
