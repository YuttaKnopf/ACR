import os
import cv2
from PIL import Image
from itertools import product

from consts.blur import (
    LAPLACIAN_VARIANCE_THRESHOLD_VALUE,
    ROBERT_VARIANCE_THRESHOLD_VALUE,
    SOBEL_VARIANCE_THRESHOLD_VALUE,
    BLUR_PERCENTAGE_THRESHOLD_VALUE,
)
from consts.divide_image import SUB_IMAGE_SIZE
from db_connections.update_object import add_disruption
from db_connections.disruptions_enum import Disruptions
from modules.blurring.laplacian_algorithm import laplacian_data
from modules.blurring.robert_algorithm import robert_data
from modules.blurring.sobel_algorithm import sobel_data
from modules.divide_image import create_sub_image
from modules.manage_folders import create_folder, remove_folder, remove_file
from modules.polygon import create_polygon


def blur_disruption(db, image_path, image_id):
    blurred_squares = []
    image_folder, file_name = os.path.split(image_path)
    image_name, extension = os.path.splitext(file_name)
    image = Image.open(image_path)
    width, height = image.size
    if is_blur_image(
        image_folder, image_name, extension, width, height, blurred_squares
    ):
        polygon = create_polygon(blurred_squares)
        add_disruption(db, image_id, Disruptions.BLUR.value, polygon)


def is_blur_image(image_folder, image_name, extension, width, height, blurred_squares):
    sum_pixels = 0
    sum_blurred_pixels = 0
    create_folder(image_name)
    grid = product(range(0, width, SUB_IMAGE_SIZE), range(0, height, SUB_IMAGE_SIZE))
    for x, y in grid:
        sub_image_pixels, sub_image_blur_pixels = blur_sub_image_algorithm(
            image_folder, image_name, extension, width, height, x, y, blurred_squares
        )
        sum_pixels += sub_image_pixels
        sum_blurred_pixels += sub_image_blur_pixels
    remove_folder(image_name)
    number_damaged_pixels = sum_blurred_pixels / sum_pixels * 100
    return number_damaged_pixels > BLUR_PERCENTAGE_THRESHOLD_VALUE


def blur_sub_image_algorithm(
    image_folder, image_name, extension, width, height, x, y, blurred_squares
):
    width_sub_image = min(x + SUB_IMAGE_SIZE, width) - x
    height_sub_image = min(y + SUB_IMAGE_SIZE, height) - y
    create_sub_image(
        x,
        y,
        f"{image_name}{extension}",
        image_folder,
        width_sub_image,
        height_sub_image,
    )
    is_blurred, is_background = detect_blurred_image(
        f"{image_name}/{image_name}_{x}_{y}{extension}"
    )
    remove_file(f"{image_name}/{image_name}_{x}_{y}{extension}")
    if is_background:
        return 0, 0
    if is_blurred:
        blurred_squares.append([(x, y), (x + width_sub_image, y + height_sub_image)])
        return width_sub_image * height_sub_image, width_sub_image * height_sub_image
    return width_sub_image * height_sub_image, 0


def detect_blurred_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred_laplacian, is_background_laplacian = is_blurred_laplacian(image)
    blurred_robert, is_background_robert = is_blurred_robert(image)
    blurred_sobel, is_background_sobel = is_blurred_sobel(image)
    if is_background_laplacian and is_background_robert and is_background_sobel:
        return False, True
    return (blurred_laplacian + blurred_robert + blurred_sobel) > 1, False


def is_blurred_laplacian(image):
    maximum, mean, variance = laplacian_data(image)
    return decide_if_blur(maximum, mean, variance, LAPLACIAN_VARIANCE_THRESHOLD_VALUE)


def is_blurred_robert(image):
    maximum, mean, variance = robert_data(image)
    return decide_if_blur(maximum, mean, variance, ROBERT_VARIANCE_THRESHOLD_VALUE)


def is_blurred_sobel(image):
    maximum, mean, variance = sobel_data(image)
    return decide_if_blur(maximum, mean, variance, SOBEL_VARIANCE_THRESHOLD_VALUE)


def decide_if_blur(maximum, mean, variance, threshold_value):
    if maximum == 0.0:
        return 0, True
    if maximum == mean or variance > threshold_value:
        return 0, False
    return 1, False
