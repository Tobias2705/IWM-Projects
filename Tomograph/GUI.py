import JpgToSin
import SinToJpg
import numpy as np
import cv2
import math
import ipywidgets as widgets
import matplotlib.pyplot as plt
from datetime import datetime
from skimage.transform import resize
from skimage.io import imread
from IPython.display import display, clear_output


# Zdefiniowanie funkcji
def normalize(image):
    min_value = np.min(image)

    max_value = np.max(image)

    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i, j] = (image[i, j] - min_value) / (max_value - min_value)

    return image


# Definicja klas
class Gui:
    def __init__(self, foto):
        self.sliders = Sliders()
        self.container = Container()
        self.startButton = StartButton()
        self.tomograph = Tomograph(360, 1, 90, 90, False, False, foto, "", "")

    def start(self):
        self.container.displayContainer.clear_output()
        self.tomograph.main()
        self.container.displayImages(self.tomograph.img, self.tomograph.sinograms[-1], self.tomograph.reverses[-1])
    
    def startProgram(self):
        self.sliders.createSlider()
        self.observeSliders()
        self.sliders.display()
        
        self.startButton.display()
        
        self.container.createContainer()
        
        self.startButton.button.on_click(self.start())

    def onSinogramChange(self, v):
        if len(self.tomograph.sinograms) < self.sliders.sinogramSlider.value or len(self.tomograph.reverses) < self.sliders.outputSlider.value:
            return
        self.container.displayImages(self.tomograph.img,
                                     self.tomograph.sinograms[self.sliders.sinogramSlider.value - 1],
                                     self.tomograph.reverses[self.sliders.outputSlider.value - 1])

    def onReverseChange(self, v):
        if len(self.tomograph.sinograms) < self.sliders.sinogramSlider.value or len(self.tomograph.reverses) < self.sliders.outputSlider.value:
            return
        self.container.displayImages(self.tomograph.img,
                                     self.tomograph.sinograms[self.sliders.sinogramSlider.value - 1],
                                     self.tomograph.reverses[self.sliders.outputSlider.value - 1])

    def onStepChange(self, v):
        self.tomograph.step = v.new

    def onDetectorsNumberChange(self, v):
        self.tomograph.detector_num = v.new

    def onDetectorsRangeChange(self, v):
        self.tomograph.detector_rng = v.new

    def observeSliders(self):
        self.sliders.sinogramSlider.observe(self.onSinogramChange, names="value")
        self.sliders.outputSlider.observe(self.onReverseChange, names="value")
        self.sliders.stepSlider.observe(self.onStepChange, names="value")
        self.sliders.detectorsNumberSlider.observe(self.onDetectorsNumberChange, names="value")
        self.sliders.detectorRangeSlider.observe(self.onDetectorsRangeChange, names="value")


class Tomograph:
    def __init__(self, iterations, step, detector_num, detector_rng, isFilter, isDicom, source, patient, descript):
        self.iterations = iterations
        self.step = step
        self.detector_num = detector_num
        self.detector_rng = detector_rng
        self.isFilter = isFilter
        self.isDicom = isDicom
        self.source = source
        self.img = None

        self.sinograms = []
        self.reverses = []
        self.original = []
        self.input_image = []

        self.patient = patient
        self.descript = descript
        self.date = datetime.now()

    def main(self):
        self.img = cv2.cvtColor(imread(self.source), cv2.COLOR_RGBA2GRAY)
        self.original = np.copy(self.img)
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
        rvr.makeReversed(sin.sinograms[-1], self.iterations, self.step, self.detector_num, self.detector_rng, dims, self.input_image)
        self.reverses = rvr.reverse_sinograms
        

    def showImage(self, title, plot):
        fig, plots = plt.subplots(1, 2)
        plots[0].imshow(self.original, cmap='gray')
        plots[0].set_title('Obraz oryginalny')
        plots[1].imshow(plot, cmap='gray')
        plots[1].set_title(title)


class Container:
    def __init__(self):
        self.displayContainer = None
        self.fig = None
        self.axes = None

    def createContainer(self):
        self.displayContainer = widgets.Output(layout={'height': '350px'})

        self.fig, self.axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

        self.axes[0].set_title('Obraz wejściowy')
        self.axes[1].set_title('Sinogram')
        self.axes[2].set_title('Obraz wyjściowy')

        self.axes[0].axis('off')
        self.axes[1].axis('off')
        self.axes[2].axis('off')

        plt.close()
        display(self.displayContainer)

    def displayImages(self, image, sinogram, reverse):
        sinogram = normalize(sinogram)
        reverse = normalize(reverse)

        with self.displayContainer:
            clear_output()
            self.axes[0].imshow(image, cmap='gray')
            self.axes[1].imshow(sinogram, cmap='gray')
            self.axes[2].imshow(reverse, cmap='gray')
            display(self.fig)


class StartButton:
    def __init__(self):
        self.button = widgets.Button(description="START", button_style="danger")

    def display(self):
        display(self.button)


class Sliders:
    def __init__(self):
        self.sinogramSlider = None
        self.outputSlider = None
        self.stepSlider = None
        self.detectorsNumberSlider = None
        self.detectorRangeSlider = None
        self.sliders = []

    def createSlider(self):
        self.sinogramSlider = widgets.IntSlider(description="Sinogram Iteration", min=1, max=360, step=1, value=360)
        self.outputSlider = widgets.IntSlider(description="Output Iteration", min=1, max=360, step=1, value=360)
        self.stepSlider = widgets.IntSlider(description="Step in degrees", min=1, max=36, step=1, value=1)
        self.detectorsNumberSlider = widgets.IntSlider(description="Number of Detectors", min=10,
                                                       max=300, step=5, value=90)
        self.detectorRangeSlider = widgets.IntSlider(description="Detectors range", min=0, max=360, step=10, value=90)

        self.sliders = [self.sinogramSlider, self.outputSlider, self.stepSlider,
                        self.detectorsNumberSlider, self.detectorRangeSlider]

    def display(self):
        for slider in self.sliders:
            box = widgets.HBox([widgets.Label(slider.description), slider])
            slider.description = ""
            display(box)
