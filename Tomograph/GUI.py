import Tomograph as Tom
import Container as Ct
import ipywidgets as widgets
import re
import time
from dateutil.parser import parse
from IPython.display import display


# Definicja klas
class Gui:
    def __init__(self, foto):
        self.sliders = Sliders()
        self.container = Ct.Container()
        self.startButton = StartButton()
        self.textFields = TextFields()
        self.checkBoxes = CheckBoxes()
        self.tomograph = Tom.Tomograph(360, 1, 90, 90, False, False, foto, "", "")

    def start(self, v):
        self.container.displayContainer.clear_output()
        self.tomograph.main()
        self.container.displayImages(self.tomograph, self.tomograph.sinograms[-1], self.tomograph.reverses[-1])
        self.displayInformation()

    def displayInformation(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Błąd średiokwadratowy: ", self.container.mse)
        if self.tomograph.patient != "":
            print("Pacjent: ", self.tomograph.patient)
            print("Opis badanego: ", self.tomograph.descript)
        print("Data badania: ", self.tomograph.date.date())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
    def startProgram(self):
        self.textFields.createTextFields(self.tomograph)
        self.observeTextFields()
        self.textFields.display()
        
        self.checkBoxes.createCheckBoxes()
        self.observerCheckBoxes()
        self.checkBoxes.display()
        
        self.sliders.createSlider()
        self.observeSliders()
        self.sliders.display()

        self.startButton.display()
        
        self.container.createContainer()

        self.startButton.button.on_click(self.start)

    def onSinogramOrReverseChange(self, v):
        if len(self.tomograph.sinograms) < self.sliders.sinogramSlider.value \
                or len(self.tomograph.reverses) < self.sliders.outputSlider.value:
            return
        time.sleep(0.2)
        self.container.displayImages(self.tomograph, self.tomograph.sinograms[self.sliders.sinogramSlider.value - 1], 
                                     self.tomograph.reverses[self.sliders.outputSlider.value - 1])

    def onStepChange(self, v):
        self.tomograph.step = v.new

    def onDetectorsNumberChange(self, v):
        self.tomograph.detector_num = v.new

    def onDetectorsRangeChange(self, v):
        self.tomograph.detector_rng = v.new

    def observeSliders(self):
        self.sliders.sinogramSlider.observe(self.onSinogramOrReverseChange, names="value")
        self.sliders.outputSlider.observe(self.onSinogramOrReverseChange, names="value")
        self.sliders.stepSlider.observe(self.onStepChange, names="value")
        self.sliders.detectorsNumberSlider.observe(self.onDetectorsNumberChange, names="value")
        self.sliders.detectorRangeSlider.observe(self.onDetectorsRangeChange, names="value")

    def updateName(self, v):
        self.tomograph.patient = self.textFields.patient.value

    def updateDescription(self, v):
        self.tomograph.descript = self.textFields.descript.value

    def updateDate(self, v):
        c1 = re.search("^[0-2][0-8]-[0][2]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # February
        c1a = re.search('^[2][9]-[0][2]-[1-2][0-9][0-9][0,2,4,6,8]$', self.textFields.date.value)  # February
        c2 = re.search("^[0-2][0-9]-[0][4,6,9]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Short months
        c3 = re.search("^[3][0]-[0][4,6,9]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Short months
        c4 = re.search("^[0-2][0-9]-[1][1]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Short months
        c5 = re.search("^[3][0]-[1][1]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Short months

        c6 = re.search("^[0-2][0-9]-[0][1,3,5,7,8]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Long months
        c7 = re.search("^[0-2][0-9]-[0][1,3,5,7,8]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Long months
        c8 = re.search("^[3][0-1]-[1][0,2]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Long months
        c9 = re.search("^[3][0-1]-[1][0,2]-[1-2][0-9][0-9][0-9]$", self.textFields.date.value)  # Long months
        if c1 or c1a or c2 or c3 or c4 or c5 or c6 or c7 or c8 or c9:
            self.tomograph.date = parse(self.textFields.date.value)

    def observeTextFields(self):
        self.textFields.patient.observe(self.updateName)
        self.textFields.descript.observe(self.updateDescription)
        self.textFields.date.observe(self.updateDate)

    def isFilteringUpdate(self, v):
        self.tomograph.isFilter = self.checkBoxes.filter.value

    def isDicomUpdate(self, v):
        self.tomograph.isDicom = self.checkBoxes.dicom.value

    def observerCheckBoxes(self):
        self.checkBoxes.filter.observe(self.isFilteringUpdate)
        self.checkBoxes.dicom.observe(self.isDicomUpdate)


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


class TextFields:
    def __init__(self):
        self.patient = None
        self.descript = None
        self.date = None
        self.fields = []

    def createTextFields(self, tom):
        self.patient = widgets.Text(description="Pacient Name", value=tom.patient)
        self.descript = widgets.Text(description="Pacient Descript", value=tom.descript)
        self.date = widgets.Text(description="Date of Medical Examination", placeholder='DD-MM-YYYY',
                                 value=tom.date.strftime("%d-%m-%Y"))

        self.fields = [self.patient, self.descript, self.date]

    def display(self):
        for text in self.fields:
            box = widgets.HBox([widgets.Label(text.description), text])
            text.description = ""
            display(box)


class CheckBoxes:
    def __init__(self):
        self.dicom = None
        self.filter = None
        self.checkBoxes = []

    def createCheckBoxes(self):
        self.dicom = widgets.Checkbox(description="DICOM", value=False)
        self.filter = widgets.Checkbox(description="Filter", value=False)

        self.checkBoxes = [self.filter, self.dicom]

    def display(self):
        box = widgets.HBox([self.filter, self.dicom])
        display(box)
