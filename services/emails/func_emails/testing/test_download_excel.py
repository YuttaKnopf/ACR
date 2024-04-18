from unittest.mock import patch, Mock
from project.download_excel import delete_blob_excel, download_blob_excel
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class MockContainer:
    def get_container_client(self, container_name):
        return MockBlob()


class MockBlob:
    def get_blob_client(self, blob_name):
        return MockBlobData()

    def delete_blob(self, blob_name):
        return


class MockBlobData:
    def download_blob(self):
        return MockDownloadedBlob()


class MockDownloadedBlob:
    def readall(self):
        return "readall"


@patch("project.get_connection_string.get_connection_string_from_keyvault")
@patch(
    "project.download_excel.BlobServiceClient.from_connection_string",
    Mock(return_value=MockContainer()),
)
def test_download_blob_excel(get_connection_string_from_keyvault):
    result = download_blob_excel("test_blob_name")
    get_connection_string_from_keyvault.assert_called()
    assert result == "readall"


@patch("project.get_connection_string.get_connection_string_from_keyvault")
@patch(
    "project.download_excel.BlobServiceClient.from_connection_string",
    Mock(return_value=MockContainer()),
)
def test_delete_blob_excel(get_connection_string_from_keyvault):
    result = delete_blob_excel("container_name", "blob_name")
    get_connection_string_from_keyvault.assert_called()
    assert result is None
