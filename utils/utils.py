from pathlib import Path
import os
import json
from typing import Dict
from cryptography.fernet import Fernet
# test
import importlib

def get_project_root() -> Path:
    """Get the root directory of the project.

    Returns:
        Path: The root directory of the project.
    """
    return Path(__file__).parent.parent

def get_global_dirs() -> dict:
    """Returns a dictionary containing all the global directories. If this file is moved, the relative import has to be adjusted.

    Returns:
        global_dirs: A dictionary containing all the global directories
    """
    ROOT_DIR = get_project_root()
    global_dirs = json.load(open(os.path.join(ROOT_DIR, "config/global_dirs.json")))

    return global_dirs

def get_config(config_file: str) -> Dict:

    """Gets the dictionary containing the configuration file contents.

    Args:
        config_file (str): The name of the configuration file as defined in the global_dirs.json file.

    Returns:
        config (dict): A dictionary containing the configuration file contents.
    """
    global_dirs = get_global_dirs()
    ROOT_DIR = get_project_root() 
    config_dir = os.path.join(ROOT_DIR, global_dirs[config_file])
    config = json.load(open(config_dir))

    return config

def get_config_py(config_file: str) -> Dict:

    """Gets the dictionary containing the configuration file .py contents.

    Args:
        config_file (str): The name of the configuration file as defined in the global_dirs.json file.

    Returns:
        config (dict): A dictionary containing the configuration file contents.
    """
    global_dirs = get_global_dirs()
    config_dir = global_dirs[config_file]
    my_config = importlib.import_module(config_dir)
    config = my_config.configs

    return config

def get_credentials() -> Dict:
    """Gets the dictionary containing the credentials file in the secrets folder.

    Returns:
        credentials: A dictionary containing the credentials file for the run.py module.
    """
    global_dirs = get_global_dirs()
    ROOT_DIR = get_project_root() 
    credentials_dir = os.path.join(ROOT_DIR, global_dirs["credentials_file"])
    credentials = json.load(open(credentials_dir))
    
    return credentials

def get_encryption_key_by_name(encryption_key_name: str) -> str:
    """Gets the encryption key from the key file located at directory defined in the config/global_dirs.json and a given key file name. Raises ValueError if key is non-existent.

    Args:
        encryption_key_name (str): The name of the encryption key file

    Returns:
        key: The encryption key in str format
    """
    global_dirs = get_global_dirs()
    ROOT_DIR = get_project_root() 
    keys_dir = os.path.join(ROOT_DIR, global_dirs["keys_dir"])
    key_file_dir = os.path.join(keys_dir, encryption_key_name)

    if os.path.isfile(key_file_dir):
        key_file_dir = open(key_file_dir, "r")
        key = key_file_dir.read()
        return key
    else:
        raise ValueError(f"The key located at {key_file_dir} does not exist")

def encrypt_string(encryption_key: str, value: str) -> str:
    """Encrypts a string given an encryption key.

    Args:
        encryption_key (str): The encryption key used to encrypt the file
        value (str): The string to be encrypted.

    Returns:
        encrypted_value: The encrypted string value. 
    """

    # Encrypt the key using Fernet module from the cryptography    
    fernet = Fernet(encryption_key)
    encrypted_value = fernet.encrypt(str.encode(value))
    
    return encrypted_value

def decrypt_string(encryption_key: str, encrypted_value: str) -> str:
    """Encrypts a string given an encryption key.

    Args:
        encryption_key (str): The encryption key used to encrypt the file
        encrypted_value (str): The string to be decrypted in byte format.

    Returns:
        decrypted_value: The decrypted string value. 
    """

    # Decrypt the key using Fernet module from the cryptography    
    fernet = Fernet(encryption_key)
    # Making sure the encrypted credential that's passed as a string gets converted to a bytestring
    encrypted_value = encrypted_value.encode()  
    decrypted_value = fernet.decrypt(encrypted_value).decode("utf-8") 

    return decrypted_value

def get_file_extension_from_path(path: str) -> str:
    """Gets file extension from directory or file name

    Args:
        path (str): The path or filename.

    Returns:
        extension (str): The extension of the file. Eg: .csv
    """
    splitted_array = os.path.splitext(path)
    extension = splitted_array[1]
    
    return extension

def get_decrypted_credential(ignored_keys: list, credential_name: str) -> dict:
    """Gets the unencrypted credentials for a particular login

    Args:
        ignored_keys (list): The list of keys to be ignored by the decryption function.
        credential_name (str): The name of the credential in the credential dictionary.

    Returns:
        decrypted_credentials (dict): A dictionary containing unencrypted credentials
    """
    encrypted_credentials = get_credentials()[credential_name]
    decrypted_credentials = encrypted_credentials.copy()
    encryption_key = get_encryption_key_by_name(encrypted_credentials["decryption_key"])
    for key in encrypted_credentials:
        if key not in ignored_keys:
            decrypted_credentials[key] = decrypt_string(encryption_key, encrypted_credentials[key])

    return decrypted_credentials
