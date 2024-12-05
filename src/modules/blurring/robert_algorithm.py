import cv2
import numpy as np


def robert_data(image):
    kernel_x = np.array([[1, 0], [0, -1]])
    kernel_y = np.array([[0, 1], [-1, 0]])
    gradient_x = cv2.filter2D(image, cv2.CV_64F, kernel_x)
    gradient_y = cv2.filter2D(image, cv2.CV_64F, kernel_y)
    robert_result = np.sqrt(gradient_x**2 + gradient_y**2)
    maximum = np.max(robert_result)
    mean = np.mean(robert_result)
    variance = np.var(robert_result)
    return maximum, mean, variance
