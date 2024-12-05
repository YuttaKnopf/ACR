import os
from datetime import datetime


def insert_image(db, photo_date, image_name, satellite):
    collection_name = os.getenv("IMAGES_COLLECTION_NAME")
    return insert_mongodb(
        db,
        collection_name,
        {
            "image_name": image_name,
            "photo_time": photo_date,
            "test_start_time": datetime.now(),
            "satellite_name": satellite,
        },
    )


def insert_mongodb(db, collection_name, insert_object):
    try:
        inserted_id = db[collection_name].insert_one(insert_object).inserted_id
        return inserted_id
    except Exception as e:
        raise Exception(f"An error occured when insert object to db: {e}")
