from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from config import config_variables
import msal


def get_connection_string_from_keyvault(secret_name):
    try:
        credentials = DefaultAzureCredential()
        client = SecretClient(config_variables.keyvault_uri, credential=credentials)
        keyVaultNameValue = client.get_secret(secret_name)
        return keyVaultNameValue.value
    except Exception as ex:
        return str(ex)


def get_access_token(client_id, client_secret, tenant_id):
    try:
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        scope = ["https://graph.microsoft.com/.default"]
        app = msal.ConfidentialClientApplication(
            client_id, authority=authority, client_credential=client_secret
        )
        result = app.acquire_token_for_client(scopes=scope)
        if "access_token" in result:
            return result["access_token"]
    except Exception as ex:
        return str(ex)
