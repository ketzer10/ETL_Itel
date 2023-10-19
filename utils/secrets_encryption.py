import utils.utils as utils
import json

def encrypt_credentials_file(ignored_keys: list) -> dict:
    """Utility function to encrypt the credentials dictionary.

    Args:
        ignored_keys (list): The keys that will not be encrypted using this method.

    Returns:
        encrypted_credentials (list): The encrypted JSON file as a Python dictionary.
    """
    credentials = utils.get_credentials()
    encrypted_credentials = credentials.copy()


    for key1 in credentials:
        for key2 in credentials[key1]:
            if key2 not in ignored_keys:
                key_name = credentials[key1]['decryption_key']
                encryption_key = utils.get_encryption_key_by_name(key_name)
                encrypted_credentials[key1][key2] = utils.encrypt_string(encryption_key, encrypted_credentials[key1][key2])

    return encrypted_credentials
    