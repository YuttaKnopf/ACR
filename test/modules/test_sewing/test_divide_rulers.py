import cv2
import pytest
import numpy as np
from unittest.mock import patch

from modules.sewing.divide_rulers import divide_rulers


@pytest.fixture
def mock_dependencies():
    mock_tiff_image = np.ones((100, 200, 3), dtype=np.uint8) * 255
    mock_gray_image = np.ones((100, 200), dtype=np.uint8) * 150
    with (
        patch("cv2.imread", return_value=mock_tiff_image) as mock_imread,
        patch("cv2.cvtColor", return_value=mock_gray_image) as mock_cvtColor,
        patch("modules.sewing.divide_rulers.NUM_SENSORS", 4),
        patch("modules.sewing.divide_rulers.NUM_COLUMNS", 10),
    ):
        yield mock_imread, mock_cvtColor, mock_tiff_image


def test_divide_rulers(mock_dependencies):
    mock_imread, mock_cvtColor, mock_tiff_image = mock_dependencies
    ruler_images = divide_rulers(mock_tiff_image)

    assert len(ruler_images) == 3
    assert ruler_images[0].shape == (100, 20)
    mock_imread.assert_called_once()
    mock_cvtColor.assert_called_once_with(mock_tiff_image, cv2.COLOR_BGR2GRAY)
