from unittest.mock import patch, call
import pytest

from modules.manage_folders import (
    create_folder,
    remove_folder,
    remove_file,
    polygon_image_path,
    get_metadata_json_file,
    get_tif_file,
)


@patch("os.path.isdir")
@patch("os.mkdir")
def test_create_folder(mock_mkdir, mock_isdir):
    mock_isdir.return_value = False
    folder_name = "test_folder"
    create_folder(folder_name)
    mock_isdir.assert_called_with(f"./{folder_name}")
    mock_mkdir.assert_called_with(f"./{folder_name}")


@patch("shutil.rmtree")
def test_remove_folder(mock_rmtree):
    folder_name = "test_folder"
    remove_folder(folder_name)
    mock_rmtree.assert_called_with(folder_name)


@patch("modules.manage_folders.os.path.exists", side_effect=[True, False])
@patch("modules.manage_folders.os.remove")
def test_remove_file(mock_remove, mock_path_exists):
    remove_file("file_name_example_1")
    remove_file("file_name_example_2")
    mock_path_exists.assert_has_calls(
        [
            call("file_name_example_1"),
            call("file_name_example_2"),
        ]
    )
    mock_remove.assert_called_once_with("file_name_example_1")


def test_polygon_image_path():
    src_path = "app/images/src/test.png"
    folder_name = "polygons/testing"
    new_path = polygon_image_path(src_path, folder_name)
    assert new_path == "app/images/polygons/testing/test.png"


@patch(
    "modules.manage_folders.os.listdir",
    return_value=["example_1_image.tif", "example_1_image_metadata.json"],
)
@patch(
    "modules.manage_folders.os.path.join",
    return_value=["images_folder/example_1_image/example_1_image_metadata.json"],
)
def test_get_metadata_json_file(mock_join, mock_listdir):
    get_metadata_json_file("images_folder/example_1_image")
    mock_listdir.assert_called_once_with("images_folder/example_1_image")
    mock_join.assert_called_once_with(
        "images_folder/example_1_image", "example_1_image_metadata.json"
    )


@patch("modules.manage_folders.os.listdir", return_value=["example_1_image.tif"])
@patch("modules.manage_folders.os.path.join")
def test_get_metadata_json_file_not_exist(mock_join, mock_listdir):
    with pytest.raises(Exception, match="Metadata.json file was not found."):
        get_metadata_json_file("images_folder/example_1_image")
    mock_listdir.assert_called_once_with("images_folder/example_1_image")
    mock_join.assert_not_called()


@patch(
    "modules.manage_folders.os.listdir",
    return_value=["example_1_image.tif", "example_1_image_metadata.json"],
)
@patch(
    "modules.manage_folders.os.path.join",
    return_value=["images_folder/example_1_image/example_1_image_metadata.json"],
)
def test_get_tif_file_file(mock_join, mock_listdir):
    get_tif_file("images_folder/example_1_image")
    mock_listdir.assert_called_once_with("images_folder/example_1_image")
    mock_join.assert_called_once_with(
        "images_folder/example_1_image", "example_1_image.tif"
    )


@patch(
    "modules.manage_folders.os.listdir", return_value=["example_1_image_metadata.json"]
)
@patch("modules.manage_folders.os.path.join")
def test_get_tif_file_not_exist(mock_join, mock_listdir):
    with pytest.raises(Exception, match=".tif file was not found."):
        get_tif_file("images_folder/example_1_image")
    mock_listdir.assert_called_once_with("images_folder/example_1_image")
    mock_join.assert_not_called()
