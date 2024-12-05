import cv2

from consts.sewing import NUM_COLUMNS, NUM_SENSORS


def divide_rulers(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    part_width = gray_image.shape[1] // NUM_SENSORS
    ruler_images = []
    for i in range(1, NUM_SENSORS):
        border_col = i * part_width
        start_col = max(0, border_col - NUM_COLUMNS)
        end_col = min(gray_image.shape[1], border_col + NUM_COLUMNS)
        border_image = gray_image[:, start_col:end_col]
        ruler_images.append(border_image)

    return ruler_images
