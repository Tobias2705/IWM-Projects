import Dicom
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
import pydicom
import math
from IPython.display import display, clear_output


# Zdefiniowanie funkcji
def normalize(image):
    min_value = np.min(image)

    max_value = np.max(image)

    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i, j] = (image[i, j] - min_value) / (max_value - min_value)

    return image


def rmse(x, y):
    MSE = np.square(np.subtract(x,y)).mean()
    RMSE = math.sqrt(MSE)
    return RMSE


class Container:
    def __init__(self):
        self.displayContainer = None
        self.fig = None
        self.axes = None
        self.rmse = None

    def createContainer(self):
        self.displayContainer = widgets.Output(layout={'height': '1050px'})

        self.fig, self.axes = plt.subplots(nrows=3, ncols=2, figsize=(25, 25))

        plt.close()
        display(self.displayContainer)

    def displayImages(self, tom, sinSlide, outSlide):
        sinogram = normalize(tom.sinograms[sinSlide])
        reverse = normalize(tom.reverses[outSlide])

        if tom.isFilter:
            sinogram = tom.filterSin[sinSlide]
            reverseF = tom.filterRes[outSlide]

        if tom.isDicom:
            Dicom.writeDicom(np.copy(reverse), tom.patient, tom.descript)
            reverseD = pydicom.dcmread("Dicom_File.dcm")
            tom.dicom = reverseD

        with self.displayContainer:
            clear_output()
            self.axes[0][0].set_title('Obraz wejściowy', fontsize=26)
            self.axes[0][1].set_title('Sinogram', fontsize=26)
            self.axes[1][0].set_title('Obraz wyjściowy bez filtru', fontsize=26)

            for i in range(3):
                for j in range(2):
                    self.axes[i][j].axis('off')
                
            self.axes[0][0].imshow(tom.original, cmap='gray')
            self.axes[0][1].imshow(sinogram, cmap='gray')
            self.axes[1][0].imshow(reverse, cmap='gray')
            
            if tom.isFilter:
                self.axes[1][1].set_visible(True)
                self.axes[1][1].set_title('Obraz wyjściowy z filtrem', fontsize=26)
                self.axes[1][1].imshow(reverseF, cmap='gray')
                self.rmse = rmse(tom.compare, reverseF)
            else:
                self.rmse = rmse(tom.compare, reverse)
                self.axes[1][1].set_visible(False)
            if tom.isDicom:
                self.axes[2][0].set_visible(True)
                self.axes[2][0].set_title('Dicom', fontsize=26)
                self.axes[2][0].imshow(reverseD.pixel_array, cmap='gray')
            else:
                self.axes[2][0].set_visible(False)
            display(self.fig)
