from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging

def retrieve_secret_from_keyvault():
    logging.info('Retrieving secret from Azure Key Vault.')

    # Azure Key Vault URL and secret name
    key_vault_url = "https://your-key-vault-name.vault.azure.net/"
    secret_name = "your-secret-name"

    try:
        # Create a DefaultAzureCredential object to authenticate
        credential = DefaultAzureCredential()

        # Create a SecretClient using the key vault URL and credential
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Get the secret value by its name
        retrieved_secret = client.get_secret(secret_name)

        # Access the secret value
        secret_value = retrieved_secret.value

        logging.info(f"Retrieved Secret Value: {secret_value}")
        return secret_value

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None
