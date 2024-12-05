import cv2
import numpy as np

from consts.saturation import (
    GRID_SIZE,
    SATURATION_THRESHOLD_VALUE,
    SATURATION_SQUARE_PERCENT,
    SATURATION_DISRUPTION_PERCENT,
)
from modules.polygon import create_polygon
from db_connections.update_object import add_disruption
from db_connections.disruptions_enum import Disruptions


def saturation_disruption(db, image_path, image_id):
    image = cv2.imread(image_path)
    saturated_image, saturated_squares = saturation_check(image)
    if saturated_image:
        polygon = create_polygon(saturated_squares)
        add_disruption(db, image_id, Disruptions.SATURATION.value, polygon)


def saturation_check(image):
    saturated_pixels, saturated_squares = saturation_check_use_grid(image)
    saturated_image = is_saturation_image(image, saturated_pixels)
    return saturated_image, saturated_squares


def saturation_check_use_grid(image):
    height, width, _ = image.shape
    sum_saturated_pixels = 0
    saturated_squares = []
    coordinates = (
        (x, y) for y in range(0, height, GRID_SIZE) for x in range(0, width, GRID_SIZE)
    )
    for x, y in coordinates:
        sum_saturated_pixels += saturated_square(image, x, y, saturated_squares)
    return sum_saturated_pixels, saturated_squares


def saturated_square(image, x, y, saturated_squares):
    square = image[y : y + GRID_SIZE, x : x + GRID_SIZE]
    saturated_pixels = calculate_saturation(square)
    if percent(saturated_pixels, square.size) >= SATURATION_SQUARE_PERCENT:
        saturated_squares.append([(x, y), (x + GRID_SIZE, y + GRID_SIZE)])
    return saturated_pixels


def calculate_saturation(square):
    saturated_pixels = np.sum(np.all(square == SATURATION_THRESHOLD_VALUE, axis=2))
    return saturated_pixels


def is_saturation_image(image, saturated_pixels):
    total_pixels = image.size / 3
    saturation_percentage = percent(saturated_pixels, total_pixels)
    return saturation_percentage >= SATURATION_DISRUPTION_PERCENT


def percent(value, total):
    if total == 0:
        return 0
    return (value / total) * 100
