from unittest.mock import patch, Mock
from project.get_connection_string import (
    get_connection_string_from_keyvault,
    get_access_token,
)


class MockClient:
    def get_secret(self, secret_name):
        return MockKeyVaultNameValue()


class MockKeyVaultNameValue:
    def __init__(self):
        self.value = "value"


@patch(
    "project.get_connection_string.DefaultAzureCredential",
    Mock(return_value="Credentials"),
)
@patch("project.get_connection_string.SecretClient", Mock(return_value=MockClient()))
def test_get_connection_string_from_keyvault():
    result = get_connection_string_from_keyvault("secret_name")
    assert result == "value"


@patch(
    "project.get_connection_string.DefaultAzureCredential",
    Mock(side_effect=Exception("can not get connection string")),
)
@patch("project.get_connection_string.SecretClient", Mock(return_value=MockClient()))
def test_get_connection_string_from_keyvault_return_error():
    result = get_connection_string_from_keyvault("secret_name")
    assert result == "can not get connection string"


class MockApp:
    def acquire_token_for_client(self, scopes):
        return {"access_token": 1}


@patch("project.get_connection_string.msal.ConfidentialClientApplication")
def test_get_access_token_ConfidentialClientApplication_called_once_with(
    ConfidentialClientApplication,
):
    get_access_token("client_id", "client_secret", "tenant_id")
    ConfidentialClientApplication.assert_called_once_with(
        "client_id",
        authority="https://login.microsoftonline.com/tenant_id",
        client_credential="client_secret",
    )


@patch(
    "project.get_connection_string.msal.ConfidentialClientApplication",
    Mock(return_value=MockApp()),
)
def test_get_access_token():
    assert get_access_token("client_id", "client_secret", "tenant_id") == 1


@patch(
    "project.get_connection_string.msal.ConfidentialClientApplication",
    Mock(side_effect=Exception("exception ConfidentialClientApplication")),
)
def test_get_access_token_return_error():
    assert (
        get_access_token("client_id", "client_secret", "tenant_id")
        == "exception ConfidentialClientApplication"
    )


# def get_access_token(client_id, client_secret, tenant_id):
#     try:
#         authority = f"https://login.microsoftonline.com/{tenant_id}"
#         scope = ["https://graph.microsoft.com/.default"]
#         app = msal.ConfidentialClientApplication(
#             client_id, authority=authority, client_credential=client_secret
#         )
#         result = app.acquire_token_for_client(scopes=scope)
#         if "access_token" in result:
#             return result["access_token"]
#     except Exception as ex:
#         return str(ex)
