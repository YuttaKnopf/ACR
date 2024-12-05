from unittest.mock import patch
from bson.objectid import ObjectId
import pytest
from pymongo import errors

from db_connections.satellite_details import get_satellite_details


class MockCollection:
    def __init__(self, returns="object"):
        self.returns = returns

    def find_one(self, company):
        match self.returns:
            case "object":
                return {
                    "_id": ObjectId("7fffffff000000000000009e"),
                    "name": "company",
                    "key": "value",
                }
            case None:
                return None
            case "error":
                raise errors.PyMongoError(
                    "An error occurred when accessing the database"
                )


@patch("db_connections.satellite_details.os.getenv", return_value="satellites")
def test_get_satellite_details(mock_getenv):
    assert get_satellite_details({"satellites": MockCollection()}, "company_name") == {
        "_id": ObjectId("7fffffff000000000000009e"),
        "name": "company",
        "key": "value",
    }
    mock_getenv.assert_called_once_with("SATELLITES_COLLECTION_NAME")


@patch("db_connections.satellite_details.os.getenv", return_value="satellites")
def test_get_satellite_details_error_handling(mock_getenv):
    with pytest.raises(
        ValueError, match="No document found for company 'wrong_company_name'"
    ):
        get_satellite_details(
            {"satellites": MockCollection(returns=None)}, "wrong_company_name"
        )

    with pytest.raises(
        errors.PyMongoError, match="An error occurred when accessing the database"
    ):
        get_satellite_details(
            {"satellites": MockCollection(returns="error")}, "company_name"
        )

    assert mock_getenv.call_count == 2
