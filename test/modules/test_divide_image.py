import numpy as np
from PIL import Image
from unittest.mock import patch, call, Mock

from modules.divide_image import (
    save_sub_image,
    create_sub_image,
)


@patch("modules.divide_image.save_sub_image")
def test_create_sub_image(mock_save_sub_image):
    create_sub_image(1, 2, "file_name.png", "temp", 10, 20)
    mock_save_sub_image.assert_called_once_with(
        "file_name.png", 1, 2, (1, 2, 11, 22), "temp"
    )


@patch("modules.divide_image.os.path.splitext", return_value=("file_name", ".png"))
@patch("modules.divide_image.Image.open")
@patch(
    "modules.divide_image.os.path.join",
    side_effect=["temp/file_name.png", "file_name/file_name_0_0.png"],
)
def test_save_sub_image(mock_join, mock_open, mock_splitext):
    image = Mock(Image.fromarray(np.zeros((100, 153, 3), dtype=np.uint8)))
    mock_open.return_value = image
    save_sub_image("file_name.png", 0, 0, (0, 0, 100, 100), "temp")
    mock_splitext.assert_called_once_with("file_name.png")
    mock_open.assert_called_once_with("temp/file_name.png")
    mock_join.assert_has_calls(
        [call("temp", "file_name.png"), call("file_name", "file_name_0_0.png")]
    )
    assert mock_join.call_count == 2
    image.crop.assert_called_once_with((0, 0, 100, 100))
    image.crop().save.assert_called_once_with("file_name/file_name_0_0.png")
