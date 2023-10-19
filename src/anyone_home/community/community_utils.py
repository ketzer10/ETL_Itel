import os
import utils.utils as utils
from subprocess import check_output
import json


def get_community_html_content(login_url, scraping_url, id_to_wait):
    # The directory of the node js script. I actually don't know what is the difference between node js and javascript.
    # Everything is going to be ok though, trust me.
    node_dir = os.path.join(utils.get_project_root(), 'src/anyone_home/community/community_scraper.js')

    try:
        creds = utils.get_decrypted_credential(['decryption_key'], 'anyone_home_community')
        username = creds['username']
        password = creds['password']

        print('Running node js script to download HTML content from community.')
        # Pass the following parameters to the node js script: 
        # login_url: The URL used to log into community.
        # username: The username used to log into community.
        # password: The password used to log into community.
        # scraping_url: The URL to the time off events report.
        # page_load_wait_time: The amount of time, in milliseconds, that the script will wait for the content of the page to load.
        html = check_output(['node', node_dir, login_url, username, password, scraping_url, id_to_wait])

        # Return the HTML but since it comes as a bytestring, decode it to UTF8
        return html.decode("utf-8")

    except Exception as e:
        print(f'Website HTML cannot be downloaded. Exception details: {e}')


def get_built_url(url_name: str, replace_params={}) -> str:
    """Gets an URL from urls.json and replaces parameters in the URL with the replaceme_params dictionary. If no replace_params
    is passed, the unmodified is returned.

    Args:
        url_name (str): The name of the URL in the JSON dictionary
        replace_params (dict, optional): A dictionary mapping the parameters of the URL. Defaults to {}. Eg. {'fdate=': '20210101'}

    Returns:
        str: [description]
    """
    ROOT_PATH = utils.get_project_root()
    urlsdir = os.path.join(ROOT_PATH, 'src/anyone_home/community/urls.json')
    urls = json.load(open(urlsdir))
    url = urls[url_name]

    for key in replace_params:
        url = url.replace(key, key+replace_params[key])

    return url


