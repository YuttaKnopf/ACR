import cv2
import numpy as np


def laplacian_data(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    maximum = np.max(laplacian)
    mean = np.mean(laplacian)
    variance = np.var(laplacian)
    return maximum, mean, variance
