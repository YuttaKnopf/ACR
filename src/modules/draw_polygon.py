import cv2
import numpy as np

from modules.manage_folders import polygon_image_path


def draw_polygons_on_image(image_path, polygons, disruptions):
    image = get_image(image_path)
    output_path = polygon_image_path(image_path, f"polygons/{disruptions}")
    match polygons["type"]:
        case "MultiPolygon":
            draw_multi_polygon(image, polygons["coordinates"], output_path)
        case "Polygon":
            draw_polygon(image, polygons["coordinates"], output_path)
        case _:
            raise Exception("It is not polygon")


def get_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or cannot be loaded")
    return image


def draw_multi_polygon(image, multi_polygon, output_path):
    for polygon in multi_polygon:
        draw_polygon(image, polygon, output_path)


def draw_polygon(image, polygon, output_path):
    for sub_polygon in polygon:
        draw_polygon_on_image(image, sub_polygon, output_path)


def draw_polygon_on_image(image, points, output_path):
    polygon_points = np.array(points, np.int32)
    polygon_points = polygon_points.reshape((-1, 1, 2))
    cv2.polylines(
        image, [polygon_points], isClosed=True, color=(0, 255, 0), thickness=2
    )
    cv2.imwrite(output_path, image)
