import numpy as np
import pydicom
from pydicom.data import get_testdata_files
import datetime

def writeDicom(image, name, comment):
    filename = get_testdata_files("CT_small.dcm")[0]
    ds = pydicom.dcmread(filename)

    def normalizeInDicom(image_temp):
        maximum = 0
        for vector in image_temp:
            if max(vector) > maximum:
                maximum = max(vector)
        for i in range(len(image_temp)):
            for x in range(len(image_temp[0])):
                if maximum != 0 and image_temp[i][x] > 0:
                    image_temp[i][x] = image_temp[i][x]*1024/maximum
                else:
                    image_temp[i][x] = 0
        return image_temp

    image = normalizeInDicom(image)
    image2 = np.asarray(image, dtype=np.uint16)
    ds.Rows = image2.shape[1]
    ds.Columns = image2.shape[0]
    ds.PixelData = image2.tostring()
    ds.PatientName = name
    ds.InstitutionName = 'Politechnika Poznanska'
    ds.Manufacturer = 'Politechnika Poznanska'
    #ds.PatientSex = sex
    #ds.PatientBirthDate = birthDate
    dt = datetime.datetime.now()
    ds.StudyDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%d')
    ds.StudyTime = timeStr
    ds.AdditionalPatientHistory = comment
    ds.save_as("Dicom_File.dcm")