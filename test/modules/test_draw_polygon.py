import cv2
import numpy as np
import os
import pytest
from unittest.mock import patch, call

from modules.draw_polygon import (
    draw_polygons_on_image,
    get_image,
    draw_multi_polygon,
    draw_polygon,
    draw_polygon_on_image,
)


def mock_image():
    return np.zeros((100, 100, 3), dtype=np.uint8)


@patch(
    "modules.draw_polygon.get_image",
    return_value="image",
)
@patch(
    "modules.draw_polygon.polygon_image_path",
    return_value="app/images/polygons/testing/test.png",
)
@patch("modules.draw_polygon.draw_multi_polygon")
@patch("modules.draw_polygon.draw_polygon")
def test_draw_polygons_on_image_when_the_type_of_polygon_is_multi_polygon(
    mock_draw_polygon, mock_draw_multi_polygon, mock_polygon_image_path, mock_get_image
):
    draw_polygons_on_image(
        "image_path",
        {"type": "MultiPolygon", "coordinates": "coordinates_points"},
        "disruptions",
    )
    mock_get_image.assert_called_once_with("image_path")
    mock_polygon_image_path.assert_called_once_with(
        "image_path", "polygons/disruptions"
    )
    mock_draw_multi_polygon.assert_called_once_with(
        "image", "coordinates_points", "app/images/polygons/testing/test.png"
    )
    mock_draw_polygon.assert_not_called()


@patch(
    "modules.draw_polygon.get_image",
    return_value="image",
)
@patch(
    "modules.draw_polygon.polygon_image_path",
    return_value="app/images/polygons/testing/test.png",
)
@patch("modules.draw_polygon.draw_multi_polygon")
@patch("modules.draw_polygon.draw_polygon")
def test_draw_polygons_on_image_when_the_type_of_polygon_is_polygon(
    mock_draw_polygon, mock_draw_multi_polygon, mock_polygon_image_path, mock_get_image
):
    draw_polygons_on_image(
        "image_path",
        {"type": "Polygon", "coordinates": "coordinates_points"},
        "disruptions",
    )
    mock_get_image.assert_called_once_with("image_path")
    mock_polygon_image_path.assert_called_once_with(
        "image_path", "polygons/disruptions"
    )
    mock_draw_multi_polygon.assert_not_called()
    mock_draw_polygon.assert_called_once_with(
        "image", "coordinates_points", "app/images/polygons/testing/test.png"
    )


@patch(
    "modules.draw_polygon.get_image",
    return_value="image",
)
@patch(
    "modules.draw_polygon.polygon_image_path",
    return_value="app/images/polygons/testing/test.png",
)
@patch("modules.draw_polygon.draw_multi_polygon")
@patch("modules.draw_polygon.draw_polygon")
def test_draw_polygons_on_image_when_the_type_of_polygon_is_not_polygon(
    mock_draw_polygon, mock_draw_multi_polygon, mock_polygon_image_path, mock_get_image
):
    with pytest.raises(Exception) as exception:
        draw_polygons_on_image(
            "image_path",
            {"type": "LineString", "coordinates": "coordinates_points"},
            "disruptions",
        )
    assert str(exception.value) == "It is not polygon"
    mock_get_image.assert_called_once_with("image_path")
    mock_polygon_image_path.assert_called_once_with(
        "image_path", "polygons/disruptions"
    )
    mock_draw_multi_polygon.assert_not_called()
    mock_draw_polygon.assert_not_called()


@patch("modules.draw_polygon.cv2.imread", return_value="image")
def test_get_image_when_image_not_None(mock_imread):
    assert get_image("image_path") == "image"
    mock_imread.assert_called_once_with("image_path")


@patch("modules.draw_polygon.cv2.imread", return_value=None)
def test_get_image_when_image_is_None(mock_imread):
    with pytest.raises(Exception) as exception:
        get_image("image_path")
    assert str(exception.value) == "Image not found or cannot be loaded"
    mock_imread.assert_called_once_with("image_path")


@patch("modules.draw_polygon.draw_polygon")
def test_draw_multi_polygon(mock_draw_polygon):
    draw_multi_polygon(
        "image",
        ["polygon_example_1", "polygon_example_2", "polygon_example_3"],
        "output_path",
    )
    assert mock_draw_polygon.call_count == 3
    mock_draw_polygon.assert_has_calls(
        [
            call("image", "polygon_example_1", "output_path"),
            call("image", "polygon_example_2", "output_path"),
            call("image", "polygon_example_3", "output_path"),
        ]
    )


@patch("modules.draw_polygon.draw_polygon_on_image")
def test_draw_polygon(mock_draw_polygon_on_image):
    draw_polygon(
        "image", ["sub_polygon_example_1", "sub_polygon_example_2"], "output_path"
    )
    assert mock_draw_polygon_on_image.call_count == 2
    mock_draw_polygon_on_image.assert_has_calls(
        [
            call("image", "sub_polygon_example_1", "output_path"),
            call("image", "sub_polygon_example_2", "output_path"),
        ]
    )


def test_draw_polygon_on_image():
    image = mock_image()
    points = [(10, 10), (30, 10), (30, 30), (10, 30)]
    output_path = "mock_image.jpg"

    draw_polygon_on_image(image, points, output_path)

    assert os.path.exists(output_path)

    saved_image = cv2.imread(output_path)
    assert saved_image is not None

    color = tuple(image[10][10])
    expected_color = (0, 255, 0)
    assert color == expected_color

    os.remove(output_path)
