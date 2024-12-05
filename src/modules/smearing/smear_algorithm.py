from PIL import Image
from itertools import product
import os
import cv2

from consts.divide_image import SUB_IMAGE_SIZE as size
from consts.smear import SMEAR_PERCENTAGE_THRESHOLD_VALUE, SMEAR_THRESHOLD_VALUE
from db_connections.update_object import add_disruption
from db_connections.disruptions_enum import Disruptions
from modules.manage_folders import create_folder, remove_file, remove_folder
from modules.divide_image import create_sub_image
from modules.smearing.check_smeared_image import compare_decay
from modules.polygon import create_polygon


def smear_disruption(db, image_path, image_id):
    smeared_squares = []
    image_folder, file_name = os.path.split(image_path)
    image_name, extension = os.path.splitext(file_name)
    image = Image.open(image_path)
    width, height = image.size

    if is_smear_image(
        image_folder, image_name, extension, width, height, smeared_squares
    ):
        polygon = create_polygon(smeared_squares)
        add_disruption(db, image_id, Disruptions.SMEAR.value, polygon)


def is_smear_image(image_folder, image_name, extension, width, height, smeared_squares):
    sum_pixels = 0
    sum_smeared_pixels = 0
    create_folder(image_name)
    grid = product(range(0, width, size), range(0, height, size))
    for x, y in grid:
        sub_image_pixels, sub_image_smear_pixels = smear_sub_image_algorithm(
            image_folder, image_name, extension, width, height, x, y, smeared_squares
        )
        sum_pixels += sub_image_pixels
        sum_smeared_pixels += sub_image_smear_pixels
    remove_folder(image_name)
    number_damaged_pixels = sum_smeared_pixels / sum_pixels * 100
    return number_damaged_pixels > SMEAR_PERCENTAGE_THRESHOLD_VALUE


def smear_sub_image_algorithm(
    image_folder, image_name, extension, width, height, x, y, smeared_squares
):
    width_sub_image = min(x + size, width) - x
    height_sub_image = min(y + size, height) - y
    create_sub_image(
        x,
        y,
        f"{image_name}{extension}",
        image_folder,
        width_sub_image,
        height_sub_image,
    )
    is_smeared, is_background = detect_smeared_image(
        f"{image_name}/{image_name}_{x}_{y}{extension}",
        image_name
    )
    remove_file(f"{image_name}/{image_name}_{x}_{y}{extension}")
    if is_background:
        return 0, 0
    if is_smeared:
        smeared_squares.append([(x, y), (x + width_sub_image, y + height_sub_image)])
        return width_sub_image * height_sub_image, width_sub_image * height_sub_image
    return width_sub_image * height_sub_image, 0


def detect_smeared_image(image_path, image_name):
    image = cv2.imread(f"{image_path}", 0)
    decay = compare_decay(image)
    if decay == 0.0:
        return False, True
    if decay < SMEAR_THRESHOLD_VALUE:
        return True, False
    return False, False
