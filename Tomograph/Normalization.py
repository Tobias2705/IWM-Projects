from skimage.transform import resize
import numpy as np


def normalization(image, frame_size=1024, img_size=624):
    frame = np.zeros([frame_size, frame_size])
    img = np.copy(image)
    img = resize(img, [img_size, img_size])
    step = int((frame_size - img_size) / 2)
    for i in range(img_size):
        for j in range(img_size):
            frame[i + step][j + step] = img[i][j]
    return frame


def normalization_smaller(image, new_size=180):
    img = np.copy(image)
    img = resize(img, [new_size, new_size])
    return img
