import pydicom
import numpy as np
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
from pydicom._storage_sopclass_uids import MRImageStorage
from datetime import datetime

def create_dicom(image, patient_name, description, DATE):
    image *= 256
    image = image.astype(np.uint16)

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    file_meta.MediaStorageSOPInstanceUID = "1.2.3"
    file_meta.ImplementationClassUID = "1.2.3.4"
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = FileDataset("output.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.PatientName = patient_name
    ds.ContentDate = DATE.strftime('%Y%m%d')
    ds.ContentTime = DATE.strftime('%H%M%S.%f')
    ds.StudyDescription = description
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.PixelRepresentation = 1
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.HighBit = 15
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SmallestImagePixelValue = str.encode('\x00\x00')
    ds.LargestImagePixelValue = str.encode('\xff\xff')
    ds.SOPClassUID = MRImageStorage
    ds.Columns = len(image)
    ds.Rows = len(image[0])

    ds.PixelData = image.tobytes()

    ds.save_as("output.dcm")