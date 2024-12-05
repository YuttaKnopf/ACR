from enum import Enum
from unittest.mock import patch, call
import numpy as np

from modules.smearing.smear_algorithm import (
    smear_disruption,
    is_smear_image,
    smear_sub_image_algorithm,
    detect_smeared_image,
)


class MockOpenImage:
    def __init__(self, width, height):
        self.size = (width, height)


class Disruptions(Enum):
    SMEAR = "smear"


@patch("modules.smearing.smear_algorithm.Disruptions", Disruptions)
@patch(
    "modules.smearing.smear_algorithm.os.path.split",
    return_value=("example/image_folder", "file_name.tiff"),
)
@patch(
    "modules.smearing.smear_algorithm.os.path.splitext",
    return_value=("file_name", ".tiff"),
)
@patch(
    "modules.smearing.smear_algorithm.Image.open", return_value=MockOpenImage(10, 20)
)
@patch("modules.smearing.smear_algorithm.is_smear_image", return_value=True)
@patch(
    "modules.smearing.smear_algorithm.create_polygon",
    return_value=[[(0, 100), (100, 100), (100, 0), (0, 0), (0, 100)]],
)
@patch("modules.smearing.smear_algorithm.add_disruption")
def test_smear_disruption_on_smeared_image(
    mock_add_disruption,
    mock_create_polygon,
    mock_is_smear_image,
    mock_open,
    mock_splitext,
    mock_split,
):
    smear_disruption("db", "example/image_folder/file_name.tiff", 1)
    mock_split.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_splitext.assert_called_once_with("file_name.tiff")
    mock_open.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_is_smear_image.assert_called_once_with(
        "example/image_folder", "file_name", ".tiff", 10, 20, []
    )
    mock_create_polygon.assert_called_once_with([])
    mock_add_disruption.assert_called_once_with(
        "db", 1, "smear", [[(0, 100), (100, 100), (100, 0), (0, 0), (0, 100)]]
    )


@patch("modules.smearing.smear_algorithm.Disruptions", Disruptions)
@patch(
    "modules.smearing.smear_algorithm.os.path.split",
    return_value=("example/image_folder", "file_name.tiff"),
)
@patch(
    "modules.smearing.smear_algorithm.os.path.splitext",
    return_value=("file_name", ".tiff"),
)
@patch(
    "modules.smearing.smear_algorithm.Image.open", return_value=MockOpenImage(10, 20)
)
@patch("modules.smearing.smear_algorithm.is_smear_image", return_value=False)
@patch(
    "modules.smearing.smear_algorithm.create_polygon",
    return_value=[[(0, 100), (100, 100), (100, 0), (0, 0), (0, 100)]],
)
@patch("modules.smearing.smear_algorithm.add_disruption")
def test_smear_disruption_on_not_smeared_image(
    mock_add_disruption,
    mock_create_polygon,
    mock_is_smear_image,
    mock_open,
    mock_splitext,
    mock_split,
):
    smear_disruption("db", "example/image_folder/file_name.tiff", 1)
    mock_split.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_splitext.assert_called_once_with("file_name.tiff")
    mock_open.assert_called_once_with("example/image_folder/file_name.tiff")
    mock_is_smear_image.assert_called_once_with(
        "example/image_folder", "file_name", ".tiff", 10, 20, []
    )
    mock_create_polygon.assert_not_called()
    mock_add_disruption.assert_not_called()


@patch("modules.smearing.smear_algorithm.size", 100)
@patch("modules.smearing.smear_algorithm.SMEAR_PERCENTAGE_THRESHOLD_VALUE", 10)
@patch("modules.smearing.smear_algorithm.create_folder")
@patch("modules.smearing.smear_algorithm.range", return_value="return from range")
@patch(
    "modules.smearing.smear_algorithm.product", return_value=[(1, 4), (2, 5), (3, 6)]
)
@patch(
    "modules.smearing.smear_algorithm.smear_sub_image_algorithm",
    side_effect=[(400, 400), (400, 0), (100, 50)],
)
@patch("modules.smearing.smear_algorithm.remove_folder")
def test_is_smear_image_when_smear(
    mock_remove_folder,
    mock_smear_sub_image_algorithm,
    mock_product,
    mock_range,
    mock_create_folder,
):
    example_smeared_squares = []
    assert is_smear_image(
        "example/image_folder", "file_name", ".tiff", 900, 850, example_smeared_squares
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
    assert mock_smear_sub_image_algorithm.call_count == 3
    mock_smear_sub_image_algorithm.assert_has_calls(
        [
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                1,
                4,
                example_smeared_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                2,
                5,
                example_smeared_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                3,
                6,
                example_smeared_squares,
            ),
        ]
    )
    mock_remove_folder.assert_called_once_with("file_name")


@patch("modules.smearing.smear_algorithm.size", 100)
@patch("modules.smearing.smear_algorithm.SMEAR_PERCENTAGE_THRESHOLD_VALUE", 10)
@patch("modules.smearing.smear_algorithm.create_folder")
@patch("modules.smearing.smear_algorithm.range", return_value="return from range")
@patch(
    "modules.smearing.smear_algorithm.product", return_value=[(1, 4), (2, 5), (3, 6)]
)
@patch(
    "modules.smearing.smear_algorithm.smear_sub_image_algorithm",
    side_effect=[(400, 0), (400, 0), (100, 50)],
)
@patch("modules.smearing.smear_algorithm.remove_folder")
def test_is_smear_image_when_not_smear(
    mock_remove_folder,
    mock_smear_sub_image_algorithm,
    mock_product,
    mock_range,
    mock_create_folder,
):
    example_smeared_squares = []
    assert not is_smear_image(
        "example/image_folder", "file_name", ".tiff", 900, 850, example_smeared_squares
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
    assert mock_smear_sub_image_algorithm.call_count == 3
    mock_smear_sub_image_algorithm.assert_has_calls(
        [
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                1,
                4,
                example_smeared_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                2,
                5,
                example_smeared_squares,
            ),
            call(
                "example/image_folder",
                "file_name",
                ".tiff",
                900,
                850,
                3,
                6,
                example_smeared_squares,
            ),
        ]
    )
    mock_remove_folder.assert_called_once_with("file_name")


@patch("modules.smearing.smear_algorithm.size", 400)
@patch("modules.smearing.smear_algorithm.min", side_effect=[400, 400])
@patch("modules.smearing.smear_algorithm.create_sub_image")
@patch(
    "modules.smearing.smear_algorithm.detect_smeared_image", return_value=(False, True)
)
@patch("modules.smearing.smear_algorithm.remove_file")
def test_smear_sub_image_algorithm_when_is_background(
    mock_remove_file, mock_detect_smeared_image, mock_create_sub_image, mock_min
):
    smeared_squares = []
    assert smear_sub_image_algorithm(
        "example/image_folder", "file_name", ".tiff", 900, 850, 0, 0, smeared_squares
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
    mock_detect_smeared_image.assert_called_once_with("file_name/file_name_0_0.tiff")
    mock_remove_file.assert_called_once_with("file_name/file_name_0_0.tiff")
    np.testing.assert_array_equal(np.array([]), smeared_squares)


@patch("modules.smearing.smear_algorithm.size", 400)
@patch("modules.smearing.smear_algorithm.min", side_effect=[900, 850])
@patch("modules.smearing.smear_algorithm.create_sub_image")
@patch(
    "modules.smearing.smear_algorithm.detect_smeared_image", return_value=(True, False)
)
@patch("modules.smearing.smear_algorithm.remove_file")
def test_smear_sub_image_algorithm_when_is_smeared(
    mock_remove_file, mock_detect_smeared_image, mock_create_sub_image, mock_min
):
    smeared_squares = []
    assert smear_sub_image_algorithm(
        "example/image_folder",
        "file_name",
        ".tiff",
        900,
        850,
        800,
        800,
        smeared_squares,
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
    mock_detect_smeared_image.assert_called_once_with(
        "file_name/file_name_800_800.tiff"
    )
    mock_remove_file.assert_called_once_with("file_name/file_name_800_800.tiff")
    np.testing.assert_array_equal(np.array([[(800, 800), (900, 850)]]), smeared_squares)


@patch("modules.smearing.smear_algorithm.size", 400)
@patch("modules.smearing.smear_algorithm.min", side_effect=[900, 850])
@patch("modules.smearing.smear_algorithm.create_sub_image")
@patch(
    "modules.smearing.smear_algorithm.detect_smeared_image", return_value=(False, False)
)
@patch("modules.smearing.smear_algorithm.remove_file")
def test_smear_sub_image_algorithm_when_is_not_smeared_and_not_background(
    mock_remove_file, mock_detect_smeared_image, mock_create_sub_image, mock_min
):
    smeared_squares = []
    assert smear_sub_image_algorithm(
        "example/image_folder",
        "file_name",
        ".tiff",
        900,
        850,
        800,
        800,
        smeared_squares,
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
    mock_detect_smeared_image.assert_called_once_with(
        "file_name/file_name_800_800.tiff"
    )
    mock_remove_file.assert_called_once_with("file_name/file_name_800_800.tiff")
    np.testing.assert_array_equal(np.array([]), smeared_squares)


@patch("modules.smearing.smear_algorithm.SMEAR_THRESHOLD_VALUE", 1200)
@patch("modules.smearing.smear_algorithm.cv2.imread", return_value="image")
@patch("modules.smearing.smear_algorithm.compare_decay", return_value=0.0)
def test_detect_smeared_image_with_background_image(
    mock_compare_decay,
    mock_imread,
):
    assert detect_smeared_image("image_name/image_name_0_0.tiff") == (False, True)
    mock_imread.assert_called_once_with("image_name/image_name_0_0.tiff", 0)
    mock_compare_decay.assert_called_once_with("image")


@patch("modules.smearing.smear_algorithm.SMEAR_THRESHOLD_VALUE", 1200)
@patch("modules.smearing.smear_algorithm.cv2.imread", return_value="image")
@patch("modules.smearing.smear_algorithm.compare_decay", return_value=1100)
def test_detect_smeared_image_with_smeared_image(
    mock_compare_decay,
    mock_imread,
):
    assert detect_smeared_image("image_name/image_name_0_0.tiff") == (True, False)
    mock_imread.assert_called_once_with("image_name/image_name_0_0.tiff", 0)
    mock_compare_decay.assert_called_once_with("image")


@patch("modules.smearing.smear_algorithm.SMEAR_THRESHOLD_VALUE", 1200)
@patch("modules.smearing.smear_algorithm.cv2.imread", return_value="image")
@patch("modules.smearing.smear_algorithm.compare_decay", return_value=1300)
def test_detect_smeared_image_with_not_smeared_image(
    mock_compare_decay,
    mock_imread,
):
    assert detect_smeared_image("image_name/image_name_0_0.tiff") == (False, False)
    mock_imread.assert_called_once_with("image_name/image_name_0_0.tiff", 0)
    mock_compare_decay.assert_called_once_with("image")
