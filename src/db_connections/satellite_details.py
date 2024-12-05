import os
from pymongo import errors


def get_satellite_details(db, company):
    try:
        collection = db[os.getenv("SATELLITES_COLLECTION_NAME")]
        document = collection.find_one({"name": company})
        if not document:
            raise ValueError(f"No document found for company '{company}'")
        return document
    except errors.PyMongoError as e:
        raise errors.PyMongoError(f"An error occurred when accessing the database: {e}")
