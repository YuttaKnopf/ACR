import shutil
import os


def create_folder(folder_name):
    if os.path.isdir(f"./{folder_name}"):
        remove_folder(folder_name)
    os.mkdir(f"./{folder_name}")


def remove_folder(folder_name):
    try:
        shutil.rmtree(folder_name)
    except OSError as e:
        raise e


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def polygon_image_path(src_path, folder_name):
    file_name = os.path.basename(src_path)
    folder_path = os.path.dirname(src_path)
    parent_folder_path = os.path.dirname(folder_path)
    polygon_image_path = os.path.join(parent_folder_path, folder_name, file_name)
    return polygon_image_path


def get_metadata_json_file(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith("metadata.json"):
            return os.path.join(folder_path, file)
    raise Exception("Metadata.json file was not found.")


def get_tif_file(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".tiff") or file.endswith(".tif"):
            return file, os.path.join(folder_path, file)
    raise Exception(".tif file was not found.")
