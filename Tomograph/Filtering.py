import numpy as np
import scipy.signal as sig
from math import floor, ceil

def do_mask(detectors):
    # maska jednowymiarowa
    mask_size = floor(detectors/2)
    mask = np.zeros(mask_size)
    center = floor(mask_size/2)
    for i in range(0, mask_size, 1):
        k = i - center
        if k % 2 != 0:
            mask[i] = (-4/np.pi**2)/k**2
    mask[center] = 1
    return mask

def filtering_sinogram(sinogram):
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    filtered = np.zeros((number_of_projections, number_of_detectors))
    mask = do_mask(number_of_detectors)
    
    # splot każdej projekcji z naszą maską
    for projection in range (number_of_projections):
        filtered[projection] = sig.convolve(sinogram[projection], mask, mode = 'same', method='direct')
    
    return filtered