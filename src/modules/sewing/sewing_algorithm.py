import numpy as np

from db_connections.update_object import add_disruption
from modules.sewing.divide_rulers import divide_rulers
from db_connections.disruptions_enum import Disruptions
from consts.sewing import (
    THRESHOLD_VALUE_DIFFERENCE,
    THRESHOLD_EXCEEDED_COLUMNS,
    PERCENT_PIXELS,
)


def sewing_disruption(db, image_path, image_id):
    ruler_images = divide_rulers(image_path)
    is_bad_sewing(db, image_id, ruler_images)


def is_bad_sewing(db, image_id, ruler_images):
    for ruler in ruler_images:
        height_image = ruler.shape[0]
        count_threshold_exceeded = check_column_disruptions(ruler, height_image)
        if count_threshold_exceeded >= THRESHOLD_EXCEEDED_COLUMNS:
            add_disruption(db, image_id, Disruptions.SEWING.value)
            return


def check_column_disruptions(ruler, height_image):
    count_threshold_exceeded = 0
    num_columns = ruler.shape[1]

    for column in range(num_columns - 1):
        percent_difference = calculate_percent_difference(
            ruler[:, column], ruler[:, column + 1], height_image
        )
        if percent_difference >= PERCENT_PIXELS:
            count_threshold_exceeded += 1

    return count_threshold_exceeded


def calculate_percent_difference(first_column, second_column, height_image):
    difference = np.abs(first_column - second_column)
    return np.sum(difference > THRESHOLD_VALUE_DIFFERENCE) / height_image * 100
