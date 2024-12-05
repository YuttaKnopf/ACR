import pytest
import numpy as np
from bson.objectid import ObjectId
from unittest.mock import patch, MagicMock

from db_connections.disruptions_enum import Disruptions
from modules.sewing.sewing_algorithm import (
    sewing_disruption,
    is_bad_sewing,
    check_column_disruptions,
    calculate_percent_difference,
)


@pytest.fixture
def mock_dependencies():
    with (
        patch("modules.sewing.sewing_algorithm.THRESHOLD_VALUE_DIFFERENCE", 120),
        patch("modules.sewing.sewing_algorithm.THRESHOLD_EXCEEDED_COLUMNS", 2),
        patch("modules.sewing.sewing_algorithm.PERCENT_PIXELS", 3),
        patch("modules.sewing.sewing_algorithm.add_disruption") as mock_add_disruption,
        patch("modules.sewing.sewing_algorithm.divide_rulers") as mock_divide_rulers,
        patch("modules.sewing.sewing_algorithm.is_bad_sewing") as mock_is_bad_sewing,
        patch(
            "modules.sewing.sewing_algorithm.calculate_percent_difference",
            return_value=2,
        ) as mock_calculate_percent_difference,
        patch(
            "modules.sewing.sewing_algorithm.check_column_disruptions", return_value=3
        ) as mock_check_column_disruptions,
    ):
        yield (
            mock_add_disruption,
            mock_divide_rulers,
            mock_is_bad_sewing,
            mock_calculate_percent_difference,
            mock_check_column_disruptions,
        )


def test_sewing_disruption(mock_dependencies):
    _, mock_divide_rulers, mock_is_bad_sewing, _, _ = mock_dependencies
    mock_image_id = "image_id"
    mock_image_path = "path/to/image.tiff"
    mock_ruler_images = [MagicMock(), MagicMock()]
    mock_divide_rulers.return_value = mock_ruler_images

    sewing_disruption("db", mock_image_path, mock_image_id)
    mock_divide_rulers.assert_called_once_with(mock_image_path)
    mock_is_bad_sewing.assert_called_once_with("db", mock_image_id, mock_ruler_images)


def test_is_bad_sewing(mock_dependencies):
    mock_add_disruption, _, _, _, mock_check_column_disruptions = mock_dependencies
    height, width = 100, 20
    ruler_image = np.zeros((height, width), dtype=np.uint8)
    ruler_image[:20, 12] = 255
    ruler_image[:20, 15] = 255
    valid_image_id = ObjectId()

    is_bad_sewing("db", valid_image_id, [ruler_image])
    mock_check_column_disruptions.assert_called_once_with(ruler_image, height)
    mock_add_disruption.assert_called_once_with(
        "db", valid_image_id, Disruptions.SEWING.value
    )

    mock_add_disruption.reset_mock()
    mock_check_column_disruptions.reset_mock()
    mock_check_column_disruptions.return_value = 1
    ruler_image = np.zeros((height, width), dtype=np.uint8)
    is_bad_sewing("db", valid_image_id, [ruler_image])
    mock_check_column_disruptions.assert_called_once_with(ruler_image, height)
    mock_add_disruption.assert_not_called()


def test_check_column_disruptions(mock_dependencies):
    _, _, _, mock_calculate_percent_difference, _ = mock_dependencies
    height_image = 100
    num_columns = 5
    ruler = np.zeros((height_image, num_columns), dtype=np.uint8)
    mock_calculate_percent_difference.side_effect = [2, 25, 1, 10]
    count_threshold_exceeded = check_column_disruptions(ruler, height_image)
    assert count_threshold_exceeded == 2
    assert mock_calculate_percent_difference.call_count == num_columns - 1


def test_calculate_percent_difference(mock_dependencies):
    height_image = 100
    first_column = np.array([5] * height_image)
    second_column = np.array([250] * 20 + [100] * 80)
    result = calculate_percent_difference(first_column, second_column, height_image)
    expected_percent_difference = (20 / height_image) * 100
    assert result == expected_percent_difference
