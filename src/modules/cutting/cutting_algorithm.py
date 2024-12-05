import cv2

from db_connections.update_object import add_disruption
from db_connections.disruptions_enum import Disruptions
from modules.cutting.classify_shape import classify_shape
from consts.cutting import SHAPE_WEIGHTS, MIN_APPROXIMATION_PERCENTAGE


def calculate_shape_similarity(image_id, image_path, target_shape):
    detected_shape = image_shape_extraction(image_path)
    if detected_shape not in SHAPE_WEIGHTS or target_shape not in SHAPE_WEIGHTS:
        raise ValueError("One or both shapes are not supported.")
    if SHAPE_WEIGHTS[target_shape][detected_shape] <= MIN_APPROXIMATION_PERCENTAGE:
        add_disruption(image_id, Disruptions.CUT_IMAGE.value)


def image_shape_extraction(image_path):
    image = cv2.imread(image_path)
    convert_to_gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(convert_to_gray_image, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        return classify_shape(approx)
    else:
        raise Exception("No contours found.")
