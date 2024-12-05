import cv2
import numpy as np


def sobel_data(image):
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    sobel_result = np.sqrt(sobelx**2 + sobely**2)
    maximum = np.max(sobel_result)
    mean = np.mean(sobel_result)
    variance = np.var(sobel_result)
    return maximum, mean, variance
