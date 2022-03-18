import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from skimage.filters import median
from sklearn.metrics import mean_squared_error


# Zdefiniowanie funkcji
def normalize(image):
    min_value = np.min(image)

    max_value = np.max(image)

    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i, j] = (image[i, j] - min_value) / (max_value - min_value)

    return image


def mse(x, y):
    err = np.sum((x.astype("float") - y.astype("float")) ** 2)
    err /= float(len(x) * len(x[0]))
    return err


class Container:
    def __init__(self):
        self.displayContainer = None
        self.fig = None
        self.axes = None
        self.mse = None

    def createContainer(self):
        self.displayContainer = widgets.Output(layout={'height': '1050px'})

        self.fig, self.axes = plt.subplots(nrows=3, ncols=2, figsize=(25, 25))

        plt.close()
        display(self.displayContainer)

    def displayImages(self, tom, sinograms, reverses):
        sinogram = normalize(sinograms)
        reverse = normalize(reverses)

        if tom.isFilter:
            reverseF = median(np.copy(reverse), selem=np.ones((5, 5)))

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
                self.mse = mse(tom.compare, reverseF)
            else:
                self.mse = mse(tom.compare, reverse)
                self.axes[1][1].set_visible(False)
            # self.axes[2][0].set_title('Obraz DICOM') -> To potem jak już dicom będziesz ogarniał
            display(self.fig)
