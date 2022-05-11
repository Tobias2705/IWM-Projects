import Segment as SGM
import numpy as np
import Image as IMG
def imageSplitting(img, holdOut):
    segments = []
    for i in range(0, len(img), 5):
        for j in range(0, len(img[0]), 5):
            segments.append(SGM.Segment(img[i : i + 5, j : j + 5], holdOut[i : i + 5, j : j + 5]))

    return segments


def prepareData(img, holdOut):
    segments = imageSplitting(img, holdOut)
    data = []
    target = []
    for segment in segments:
        data.append(segment.getData())
        target.append(segment.isVesselBin)

    return np.array(data).astype(np.uint8), np.array(target).astype(np.uint8)

def preparedtraindata(img_list, holdOut_list):
    image2 = IMG.Image()
    data = []
    target = []
    for i in range(10):
        image2.imageProcess(img_list[i], holdOut_list[i])
        img = image2.prepared
        holdOut = image2.holdOut
        segments = imageSplitting(img, holdOut)
        for segment in segments:
            data.append(segment.getData())
            target.append(segment.isVesselBin)

    return np.array(data).astype(np.uint8), np.array(target).astype(np.uint8)