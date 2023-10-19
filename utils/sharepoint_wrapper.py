from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import io
import utils.utils as utils

from utils.utils import get_file_extension_from_path

def get_sharepoint_ctx(site_url: str, username: str, password:str) -> ClientContext:
    """ Gets a SharePoint ClientContext object given a site url, username and password combination.
    Args:
        site_url (str): The URL of the SharePoint site. Eg: https://itelbposmartsolutions.sharepoint.com/sites/DataScienceHub/
        username (str): The username of the Office 365 account that owns the SharePoint site.
        password (str): The password of the Office 365 account.

    Returns:
        web (ClientContext): Represents a SharePoint client context object.
    """
    try:
        ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
    except Exception as e:
        raise Exception(f"Could not fetch SharePoint client context. {e}")

    return ctx

def get_datascience_hub_ctx() -> ClientContext:
    """ Gets the SharePoint ClientContext object for the Data Science Hub site using the reporting@itelinternational.com 
    account. This is a convenience method used to connect to the Data Science Hub SharePoint directly.

    Returns:
        [ClientContext]: A SharePoint ClientContext object referencing the Data Science Hub SharePoint site.
    """
    
    sharepoint_configs = utils.get_config('dshub_sharepoint_config')
    sh_credentials = utils.get_decrypted_credential(['decryption_key'], 'data_science_hub_credentials')
    ctx = get_sharepoint_ctx(sharepoint_configs['sharepoint_site']['site_url'], sh_credentials['username'], 
                             sh_credentials['password'])

    return ctx


def get_sharepoint_file_by_id(context_object: ClientContext, file_id: str) -> dict:
    """Gets a SharePoint file given a GUID. Returns a dictionary containing a bytestream that contains 
    the contents of the file and the extension of the file.

    Args:
        context_object (ClientContext): The SharePoint context object.
        file_id (str): The GUID of the file to be downloaded.

    Raises:
        Exception: On any HTTP response code not 200.

    Returns:
        data [dict]: A dictionary containing three keys: 'contents', 'extension' and 'file_name. 'contents' contains a bytestream 
        representation of the file. 'extension' contains the extension of the file as extracted from the name and 'file_name'
        contains the name of the file as appears on the SharePoint site.
    """

    try:

        # Get the file object from the SharePoint website using the ID
        file_obj = context_object.web.get_file_by_id(file_id)
        context_object.load(file_obj).execute_query()

        # Get the extension of the file
        file_extension = get_file_extension_from_path(file_obj.name)
        
        # Get the name of the file on Sharepoint
        file_name = file_obj.properties["Name"]
        
        # Request the file object, returns an HTTP response object.
        response = File.open_binary(context_object, file_obj.serverRelativeUrl)

        # Raise exception if status code is not 200
        if response.status_code != 200:
            raise Exception(f"Couldn't fetch file with ID {file_id}")

        # Write the contents of the response into a bytestream
        byte_stream = io.BytesIO(response.content)

    except Exception as e:
        raise Exception(f"Couldn't fetch SharePoint file by ID. {e}")

    # Store the data in a dictionary for readability and accesibility in other functions
    data = {
        'contents': byte_stream,
        'extension': file_extension,
        'file_name': file_name
    }

    return data

def get_files_by_folder_id(context_object: ClientContext, folder_id: str) -> list:
    """Gets all the files GUIDs (not folders) in a given folder ID

    Args:
        context_object (ClientContext): The SharePoint context object.
        folder_id (str): The ID of the folder.

    Returns:
        file_ids (list): A list containing the GUID of every file in the folder
    """
    # Get the folder object 
    folder_obj = context_object.web.get_folder_by_id(folder_id)
    context_object.load(folder_obj).execute_query()
    files_collection = folder_obj.files
    context_object.load(files_collection).execute_query()

    file_ids = [file.properties['UniqueId'] for file in files_collection]

    return file_ids

def get_files_names_extensiones_and_ids_by_folder_id(context_object: ClientContext, folder_id: str) -> list:
    """Gets all the files GUIDs (not folders) in a given folder ID

    Args:
        context_object (ClientContext): The SharePoint context object.
        folder_id (str): The ID of the folder.

    Returns:
        file_ids (list): A list containing the GUID of every file in the folder (Name, Extension, UniqueID)
    """
    # Get the folder object 
    folder_obj = context_object.web.get_folder_by_id(folder_id)
    context_object.load(folder_obj).execute_query()
    files_collection = folder_obj.files
    context_object.load(files_collection).execute_query()

    file_names_extensions_and_ids = [(file.properties['Name'], get_file_extension_from_path(file.properties['Name']), file.properties['UniqueId']) for file in files_collection]

    return sorted(file_names_extensions_and_ids)


def move_file_to_folder(context_object: ClientContext, dest_folder_id: str, file_id: File) -> str:
    """Moves file to a folder given a file ID and a folder ID

    Args:
        context_object (ClientContext): The SharePoint context object.
        dest_folder_id (str): The GUID of the destination folder.
        file_id (File): The GUID of the file to be moved
    """
    
    try:
        # Get the destination folder Folder object and the relative URL
        folder_obj = context_object.web.get_folder_by_id(dest_folder_id)
        context_object.load(folder_obj).execute_query()

        folder_obj_url = folder_obj.properties['ServerRelativeUrl']

        # Get the file object by ID and the relative path
        file_obj = context_object.web.get_file_by_id(file_id)
        context_object.load(file_obj).execute_query()

        # Construct the destination folder+file URL
        destination_path = folder_obj_url + '/' + file_obj.name

        # Move the file
        file_obj.moveto(destination_path, 1)
        context_object.execute_query()
        print('File moved')
    except Exception as e:
        print(e)
        print('File not moved')

def get_folders_by_folder_id(context_object: ClientContext, folder_id: str) -> dict:

    """Gets all the folder names, ids and paths in a given folder ID
    Args:
        context_object (ClientContext): The SharePoint context object.
        folder_id (str): The ID of the folder.

    Returns:
        data (dict): A dictionary of strings containing Folder Name (folder_name), 
        Folder UID (folder_id) and Server Relative Path(server_relative_url)

    """
    # Get the folder object
    folder_obj = context_object.web.get_folder_by_id(folder_id)
    context_object.load(folder_obj).execute_query()
    folder_collection = folder_obj.folders
    context_object.load(folder_collection).execute_query()

    folder_ids = [folder.properties['UniqueId'] for folder in folder_collection]
    folder_names = [folder.properties['Name'] for folder in folder_collection]
    server_urls = [folder.properties['ServerRelativeUrl'] for folder in folder_collection]

    data = {
        "folder_name":folder_names,
        "folder_id":folder_ids,
        "server_relative_url":server_urls
    }

    return data


def upload_file_to_sharepoint_folder(context_object: ClientContext, folder_id: str, file_name: str, file):
    """Uploads a file to a target sharepoint folder

    Args:
        context_object (ClientContext): The SharePoint context object.
        folder_id (str): The ID of the folder
        file_name (str): Name of the file to be written, including extension
        file (_type_): File to be uploaded
    """
    try:
        folder_obj = context_object.web.get_folder_by_id(folder_id)
        context_object.load(folder_obj).execute_query()

        folder_obj_url = folder_obj.properties['ServerRelativeUrl'] 

        print("Writing", folder_obj_url + "/" + file_name)
        folder_obj.upload_file(file_name, file).execute_query()
        print("File written")

    except Exception as e:
        print(e)
        print("File not written")


def create_folder_in_sharepoint(context_object: ClientContext, folder_id: str, folder_name: str):
    """Creates a folder in sharepoint at a target location

    Args:
        context_object (ClientContext): The SharePoint context object.
        folder_id (str): The folder of ID of the location where the new folder will be created
        folder_name (str): Name of the new folder
    """
    try:
        folder_obj = context_object.web.get_folder_by_id(folder_id)
        context_object.load(folder_obj).execute_query()

        folder_obj_url = folder_obj.properties['ServerRelativeUrl'] 

        output_folder = folder_obj_url + "/" + folder_name

        print("Creating", output_folder)
        folder_obj.folders.add(output_folder).execute_query()
        print("Created folder")

    except Exception as e:
        print(e)
        print("Folder not written")        