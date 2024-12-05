from enum import Enum
from unittest.mock import patch, call
import numpy as np

from modules.blurring.blur_algorithm import (
    blur_disruption,
    is_blur_image,
    blur_sub_image_algorithm,
    detect_blurred_image,
    is_blurred_laplacian,
    is_blurred_robert,
    is_blurred_sobel,
    decide_if_blur,
)


class MockOpenImage:
    def __init__(self, width, height):
        self.size = (width, height)


class Disruptions(Enum):
    BLUR = "blur"


@patch("modules.blurring.blur_algorithm.Disruptions", Disruptions)
@patch(
    "modules.blurring.blur_algorithm.os.path.split",
    return_value=("example/image_folder", "file_name.tiff"),
)
@patch(
    "modules.blurring.blur_algorithm.os.path.splitext",
    return_value=("file_name", ".tiff"),
)
@patch("modules.blurring.blur_algorithm.Image.open", return_value=MockOpenImage(10, 20))
@patch("modules.blurring.blur_algorithm.is_blur_image", return_value=True)
@patch(
    "modules.blurring.blur_algorithm.create_polygon",
    return_value=[[(0, 100), (100, 100), (100, 0), (0, 0), (0, 100)]],
)
@patch("modules.blurring.blur_algorithm.add_disruption")
def test_blur_disruption_on_image_blur(
    mock_add_disruption,
    mock_create_polygon,
    mock_is_blur_image,
    mock_open,
    mock_splitext,
    mock_split,
):
    blur_disruption("db", "example/image_folder/file_name.tiff", 1)
    mock_split.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_splitext.assert_called_once_with("file_name.tiff")
    mock_open.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_is_blur_image.assert_called_once_with(
        "example/image_folder", "file_name", ".tiff", 10, 20, []
    )
    mock_create_polygon.assert_called_once_with([])
    mock_add_disruption.assert_called_once_with(
        "db", 1, "blur", [[(0, 100), (100, 100), (100, 0), (0, 0), (0, 100)]]
    )


@patch("modules.blurring.blur_algorithm.Disruptions", Disruptions)
@patch(
    "modules.blurring.blur_algorithm.os.path.split",
    return_value=("example/image_folder", "file_name.tiff"),
)
@patch(
    "modules.blurring.blur_algorithm.os.path.splitext",
    return_value=("file_name", ".tiff"),
)
@patch("modules.blurring.blur_algorithm.Image.open", return_value=MockOpenImage(10, 20))
@patch("modules.blurring.blur_algorithm.is_blur_image", return_value=False)
@patch(
    "modules.blurring.blur_algorithm.create_polygon",
    return_value=[[(0, 100), (100, 100), (100, 0), (0, 0), (0, 100)]],
)
@patch("modules.blurring.blur_algorithm.add_disruption")
def test_blur_disruption_on_image_not_blur(
    mock_add_disruption,
    mock_create_polygon,
    mock_is_blur_image,
    mock_open,
    mock_splitext,
    mock_split,
):
    blur_disruption("db", "example/image_folder/file_name.tiff", 1)
    mock_split.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_splitext.assert_called_once_with("file_name.tiff")
    mock_open.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_is_blur_image.assert_called_once_with(
        "example/image_folder", "file_name", ".tiff", 10, 20, []
    )
    mock_create_polygon.assert_not_called()
    mock_add_disruption.assert_not_called()


@patch("modules.blurring.blur_algorithm.SUB_IMAGE_SIZE", 100)
@patch("modules.blurring.blur_algorithm.BLUR_PERCENTAGE_THRESHOLD_VALUE", 10)
@patch("modules.blurring.blur_algorithm.create_folder")
@patch("modules.blurring.blur_algorithm.range", return_value="return from range")
@patch("modules.blurring.blur_algorithm.product", return_value=[(1, 4), (2, 5), (3, 6)])
@patch(
    "modules.blurring.blur_algorithm.blur_sub_image_algorithm",
    side_effect=[(400, 400), (400, 0), (100, 50)],
)
@patch("modules.blurring.blur_algorithm.remove_folder")
def test_is_blur_image_when_blur(
    mock_remove_folder,
    mock_blur_sub_image_algorithm,
    mock_product,
    mock_range,
    mock_create_folder,
):
    example_blurred_squares = []
    assert is_blur_image(
        "example/image_folder", "file_name", ".tiff", 900, 850, example_blurred_squares
    )
    mock_create_folder.assert_called_once_with("file_name")
    assert mock_range.call_count == 2
    mock_range.assert_has_calls(
        [
            call(0, 900, 100),
            call(0, 850, 100),
        ]
    )
    mock_product.assert_called_once_with("return from range", "return from range")
    assert mock_blur_sub_image_algorithm.call_count == 3
    mock_blur_sub_image_algorithm.assert_has_calls(
        [
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                1,
                4,
                example_blurred_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                2,
                5,
                example_blurred_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                3,
                6,
                example_blurred_squares,
            ),
        ]
    )
    mock_remove_folder.assert_called_once_with("file_name")


@patch("modules.blurring.blur_algorithm.SUB_IMAGE_SIZE", 100)
@patch("modules.blurring.blur_algorithm.BLUR_PERCENTAGE_THRESHOLD_VALUE", 10)
@patch("modules.blurring.blur_algorithm.create_folder")
@patch("modules.blurring.blur_algorithm.range", return_value="return from range")
@patch("modules.blurring.blur_algorithm.product", return_value=[(1, 4), (2, 5), (3, 6)])
@patch(
    "modules.blurring.blur_algorithm.blur_sub_image_algorithm",
    side_effect=[(400, 0), (400, 0), (100, 50)],
)
@patch("modules.blurring.blur_algorithm.remove_folder")
def test_is_blur_image_when_not_blur(
    mock_remove_folder,
    mock_blur_sub_image_algorithm,
    mock_product,
    mock_range,
    mock_create_folder,
):
    example_blurred_squares = []
    assert not is_blur_image(
        "example/image_folder", "file_name", ".tiff", 900, 850, example_blurred_squares
    )
    mock_create_folder.assert_called_once_with("file_name")
    assert mock_range.call_count == 2
    mock_range.assert_has_calls(
        [
            call(0, 900, 100),
            call(0, 850, 100),
        ]
    )
    mock_product.assert_called_once_with("return from range", "return from range")
    assert mock_blur_sub_image_algorithm.call_count == 3
    mock_blur_sub_image_algorithm.assert_has_calls(
        [
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                1,
                4,
                example_blurred_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                2,
                5,
                example_blurred_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                3,
                6,
                example_blurred_squares,
            ),
        ]
    )
    mock_remove_folder.assert_called_once_with("file_name")


@patch("modules.blurring.blur_algorithm.SUB_IMAGE_SIZE", 400)
@patch("modules.blurring.blur_algorithm.min", side_effect=[400, 400])
@patch("modules.blurring.blur_algorithm.create_sub_image")
@patch(
    "modules.blurring.blur_algorithm.detect_blurred_image", return_value=(False, True)
)
@patch("modules.blurring.blur_algorithm.remove_file")
def test_blur_sub_image_algorithm_when_is_background(
    mock_remove_file, mock_detect_blurred_image, mock_create_sub_image, mock_min
):
    blurred_squares = []
    assert blur_sub_image_algorithm(
        "example/image_folder", "file_name", ".tiff", 900, 850, 0, 0, blurred_squares
    ) == (0, 0)
    assert mock_min.call_count == 2
    mock_min.assert_has_calls(
        [
            call(400, 900),
            call(400, 850),
        ]
    )
    mock_create_sub_image.assert_called_once_with(
        0, 0, "file_name.tiff", "example/image_folder", 400, 400
    )
    mock_detect_blurred_image.assert_called_once_with("file_name/file_name_0_0.tiff")
    mock_remove_file.assert_called_once_with("file_name/file_name_0_0.tiff")
    np.testing.assert_array_equal(np.array([]), blurred_squares)


@patch("modules.blurring.blur_algorithm.SUB_IMAGE_SIZE", 400)
@patch("modules.blurring.blur_algorithm.min", side_effect=[900, 850])
@patch("modules.blurring.blur_algorithm.create_sub_image")
@patch(
    "modules.blurring.blur_algorithm.detect_blurred_image", return_value=(True, False)
)
@patch("modules.blurring.blur_algorithm.remove_file")
def test_blur_sub_image_algorithm_when_is_blurred(
    mock_remove_file, mock_detect_blurred_image, mock_create_sub_image, mock_min
):
    blurred_squares = []
    assert blur_sub_image_algorithm(
        "example/image_folder",
        "file_name",
        ".tiff",
        900,
        850,
        800,
        800,
        blurred_squares,
    ) == (5000, 5000)
    assert mock_min.call_count == 2
    mock_min.assert_has_calls(
        [
            call(1200, 900),
            call(1200, 850),
        ]
    )
    mock_create_sub_image.assert_called_once_with(
        800, 800, "file_name.tiff", "example/image_folder", 100, 50
    )
    mock_detect_blurred_image.assert_called_once_with(
        "file_name/file_name_800_800.tiff"
    )
    mock_remove_file.assert_called_once_with("file_name/file_name_800_800.tiff")
    np.testing.assert_array_equal(np.array([[(800, 800), (900, 850)]]), blurred_squares)


@patch("modules.blurring.blur_algorithm.SUB_IMAGE_SIZE", 400)
@patch("modules.blurring.blur_algorithm.min", side_effect=[900, 850])
@patch("modules.blurring.blur_algorithm.create_sub_image")
@patch(
    "modules.blurring.blur_algorithm.detect_blurred_image", return_value=(False, False)
)
@patch("modules.blurring.blur_algorithm.remove_file")
def test_blur_sub_image_algorithm_when_is_not_blurred_and_not_background(
    mock_remove_file, mock_detect_blurred_image, mock_create_sub_image, mock_min
):
    blurred_squares = []
    assert blur_sub_image_algorithm(
        "example/image_folder",
        "file_name",
        ".tiff",
        900,
        850,
        800,
        800,
        blurred_squares,
    ) == (5000, 0)
    assert mock_min.call_count == 2
    mock_min.assert_has_calls(
        [
            call(1200, 900),
            call(1200, 850),
        ]
    )
    mock_create_sub_image.assert_called_once_with(
        800, 800, "file_name.tiff", "example/image_folder", 100, 50
    )
    mock_detect_blurred_image.assert_called_once_with(
        "file_name/file_name_800_800.tiff"
    )
    mock_remove_file.assert_called_once_with("file_name/file_name_800_800.tiff")
    np.testing.assert_array_equal(np.array([]), blurred_squares)


@patch("modules.blurring.blur_algorithm.cv2.IMREAD_GRAYSCALE", 0)
@patch("modules.blurring.blur_algorithm.cv2.imread", return_value="image")
@patch("modules.blurring.blur_algorithm.is_blurred_laplacian", return_value=(0, True))
@patch("modules.blurring.blur_algorithm.is_blurred_robert", return_value=(0, True))
@patch("modules.blurring.blur_algorithm.is_blurred_sobel", return_value=(0, True))
def test_detect_blurred_image_with_background_image(
    mock_is_blurred_sobel,
    mock_is_blurred_robert,
    mock_is_blurred_laplacian,
    mock_imread,
):
    assert detect_blurred_image("image_name/image_name_0_0.tiff") == (False, True)
    mock_imread.assert_called_once_with("image_name/image_name_0_0.tiff", 0)
    mock_is_blurred_laplacian.assert_called_once_with("image")
    mock_is_blurred_robert.assert_called_once_with("image")
    mock_is_blurred_sobel.assert_called_once_with("image")


@patch("modules.blurring.blur_algorithm.cv2.IMREAD_GRAYSCALE", 0)
@patch("modules.blurring.blur_algorithm.cv2.imread", return_value="image")
@patch("modules.blurring.blur_algorithm.is_blurred_laplacian", return_value=(0, False))
@patch("modules.blurring.blur_algorithm.is_blurred_robert", return_value=(1, False))
@patch("modules.blurring.blur_algorithm.is_blurred_sobel", return_value=(1, False))
def test_detect_blurred_image_with_blurred_image(
    mock_is_blurred_sobel,
    mock_is_blurred_robert,
    mock_is_blurred_laplacian,
    mock_imread,
):
    assert detect_blurred_image("image_name/image_name_0_0.tiff") == (True, False)
    mock_imread.assert_called_once_with("image_name/image_name_0_0.tiff", 0)
    mock_is_blurred_laplacian.assert_called_once_with("image")
    mock_is_blurred_robert.assert_called_once_with("image")
    mock_is_blurred_sobel.assert_called_once_with("image")


@patch("modules.blurring.blur_algorithm.cv2.IMREAD_GRAYSCALE", 0)
@patch("modules.blurring.blur_algorithm.cv2.imread", return_value="image")
@patch("modules.blurring.blur_algorithm.is_blurred_laplacian", return_value=(0, False))
@patch("modules.blurring.blur_algorithm.is_blurred_robert", return_value=(1, False))
@patch("modules.blurring.blur_algorithm.is_blurred_sobel", return_value=(0, False))
def test_detect_blurred_image_with_not_blurred_image(
    mock_is_blurred_sobel,
    mock_is_blurred_robert,
    mock_is_blurred_laplacian,
    mock_imread,
):
    assert detect_blurred_image("image_name/image_name_0_0.tiff") == (False, False)
    mock_imread.assert_called_once_with("image_name/image_name_0_0.tiff", 0)
    mock_is_blurred_laplacian.assert_called_once_with("image")
    mock_is_blurred_robert.assert_called_once_with("image")
    mock_is_blurred_sobel.assert_called_once_with("image")


@patch("modules.blurring.blur_algorithm.LAPLACIAN_VARIANCE_THRESHOLD_VALUE", 3)
@patch("modules.blurring.blur_algorithm.laplacian_data", return_value=(50, 25, 20))
@patch("modules.blurring.blur_algorithm.decide_if_blur", return_value=(0, False))
def test_is_blurred_laplacian(mock_decide_if_blur, mock_laplacian_data):
    assert is_blurred_laplacian("image_name/image_name_0_0.tiff") == (0, False)
    mock_laplacian_data.assert_called_once_with("image_name/image_name_0_0.tiff")
    mock_decide_if_blur.assert_called_once_with(50, 25, 20, 3)


@patch("modules.blurring.blur_algorithm.ROBERT_VARIANCE_THRESHOLD_VALUE", 8)
@patch("modules.blurring.blur_algorithm.robert_data", return_value=(12, 12, 5))
@patch("modules.blurring.blur_algorithm.decide_if_blur", return_value=(1, False))
def test_is_blurred_robert(mock_decide_if_blur, mock_robert_data):
    assert is_blurred_robert("image_name/image_name_0_0.tiff") == (1, False)
    mock_robert_data.assert_called_once_with("image_name/image_name_0_0.tiff")
    mock_decide_if_blur.assert_called_once_with(12, 12, 5, 8)


@patch("modules.blurring.blur_algorithm.SOBEL_VARIANCE_THRESHOLD_VALUE", 300)
@patch("modules.blurring.blur_algorithm.sobel_data", return_value=(0.0, 0.0, 0.0))
@patch("modules.blurring.blur_algorithm.decide_if_blur", return_value=(0, True))
def test_is_blurred_sobel(mock_decide_if_blur, mock_sobel_data):
    assert is_blurred_sobel("image_name/image_name_0_0.tiff") == (0, True)
    mock_sobel_data.assert_called_once_with("image_name/image_name_0_0.tiff")
    mock_decide_if_blur.assert_called_once_with(0.0, 0.0, 0.0, 300)


def test_decide_if_blur_when_all_image_is_one_color():
    assert decide_if_blur(5, 5, 5, 3) == (0, False)


def test_decide_if_blur_when_the_image_background():
    assert decide_if_blur(0, 0, 0, 9) == (0, True)


def test_decide_if_blur_when_the_image_blur():
    assert decide_if_blur(5, 3, 4, 8) == (1, False)


def test_decide_if_blur_when_the_image_not_blur():
    assert decide_if_blur(5, 3, 4, 3) == (0, False)
