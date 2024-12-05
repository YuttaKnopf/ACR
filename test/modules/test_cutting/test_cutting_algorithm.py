import pytest
from unittest.mock import patch, MagicMock

from modules.cutting.cutting_algorithm import calculate_shape_similarity


@pytest.fixture
def mock_dependencies():
    with (
        patch("cv2.imread", return_value=MagicMock()) as mock_imread,
        patch(
            "modules.cutting.cutting_algorithm.classify_shape", return_value="Rectangle"
        ) as mock_classify_shape,
        patch(
            "modules.cutting.cutting_algorithm.cv2.findContours"
        ) as mock_findContours,
        patch(
            "modules.cutting.cutting_algorithm.add_disruption"
        ) as mock_add_disruption,
        patch(
            "modules.cutting.cutting_algorithm.image_shape_extraction"
        ) as mock_image_shape_extractions,
        patch(
            "modules.cutting.cutting_algorithm.MIN_APPROXIMATION_PERCENTAGE", 70
        ) as mock_min_approximation_percentage,
        patch(
            "modules.cutting.cutting_algorithm.SHAPE_WEIGHTS",
            {
                "triangle": {"triangle": 100, "rectangle": 50},
                "rectangle": {"triangle": 50, "rectangle": 100},
            },
        ) as mock_shape_weights,
    ):
        yield (
            mock_imread,
            mock_classify_shape,
            mock_findContours,
            mock_add_disruption,
            mock_image_shape_extractions,
            mock_min_approximation_percentage,
            mock_shape_weights,
        )


def test_calculate_shape_similarity(mock_dependencies):
    (
        _,
        _,
        _,
        mock_add_disruption,
        mock_image_shape_extractions,
        _,
        _,
    ) = mock_dependencies
    mock_image_shape_extractions.return_value = "triangle"
    calculate_shape_similarity(
        image_id="_123", image_path="test_path.tiff", target_shape="triangle"
    )
    mock_add_disruption.assert_not_called()
    mock_add_disruption.reset_mock()
    calculate_shape_similarity(
        image_id="_123", image_path="test_path.tiff", target_shape="rectangle"
    )
    mock_add_disruption.assert_called_once_with("_123", "cut_image")
