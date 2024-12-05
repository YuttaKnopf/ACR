import os
from dotenv import load_dotenv

from db_connections.connection import connect, disconnect
from db_connections.insert_object import insert_image
from db_connections.update_object import add_end_date_value
from db_connections.satellite_details import get_satellite_details
from modules.extract_value import get_value_by_keys, get_company_by_image_name
from modules.blurring.blur_algorithm import blur_disruption
from modules.manage_folders import get_metadata_json_file, get_tif_file
from modules.saturation.saturation_algorithm import saturation_disruption
from modules.smearing.smear_algorithm import smear_disruption

load_dotenv()


def main():
    try:
        db = connect()
        images_path = os.getenv("IMAGES_PATH")
        for image_folder in os.listdir(images_path):
            check_image(db, images_path, image_folder)
        disconnect()
    except Exception:
        pass


def check_image(db, images_path, image_folder):
    try:
        (
            json_file_path,
            tiff_file_name,
            image_path,
            satellite_name,
            satellite_details,
        ) = get_image_data(db, images_path, image_folder)
        mongo_image_id = insert_image_to_mongo(
            db,
            tiff_file_name,
            json_file_path,
            satellite_details["date_location"],
            satellite_name,
        )
        print("mongo_image_id")
        print(mongo_image_id)
        print(mongo_image_id)
        print("mongo_image_id")
    except Exception:
        return
    send_to_check_disruptions(db, image_path, mongo_image_id)
    add_end_date_value(db, mongo_image_id)


def get_image_data(db, images_path, image_folder):
    json_file_path = get_metadata_json_file(f"{images_path}/{image_folder}")
    tiff_file, image_path = get_tif_file(f"{images_path}/{image_folder}")
    satellite_name = get_company_by_image_name(tiff_file)
    satellite_details = get_satellite_details(db, satellite_name)
    tiff_file_name = os.path.splitext(tiff_file)[0]
    return json_file_path, tiff_file_name, image_path, satellite_name, satellite_details


def insert_image_to_mongo(db, image_name, json_file_path, date_keys, satellite_name):
    try:
        try:
            date = get_value_by_keys(json_file_path, date_keys)
        except Exception:
            date = None
        return insert_image(db, date, image_name, satellite_name)
    except Exception as e:
        raise e


def send_to_check_disruptions(db, image_path, mongo_image_id):
    for disruption in [
        blur_disruption,
        smear_disruption,
        saturation_disruption,
    ]:
        try:
            disruption(db, image_path, mongo_image_id)
        except Exception:
            continue


if __name__ == "__main__":
    main()
