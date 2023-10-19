import os

import utils.utils as utils
import utils.seleniumutils as seleniumutils
import utils.sharepoint_wrapper as sharepoint_wrapper

from selenium.webdriver.common.keys import Keys
from time import sleep


file1 = open('./secrets/keys/public.key', 'rb')  # Open the file as wb to read bytes
DECRIPTION_KEY = file1.read()  # The key will be type bytes

#user = os.path.expanduser()

WEBPROFILE = os.path.expanduser(r'~/AppData/Local/Google/Chrome/User Data')
WEBDRIVERPATH = 'C:/Users/David.Nolasco/Desktop/Python test/Automation_Scripts/Dependencies/Chrome Driver/chromedriver.exe'

FILEFOLDER = 'C:/Users/David.Nolasco/Desktop/Python test/Automation_Scripts/downloads'
SHAREPOINT_FOLDER = 'coadvantage_timesheet'

def main(optional: list):
    """ Runs the navigate_n_download.
    Args:
        optional (int): Run mode. 
    """

    credentials = utils.get_credentials()['kronos_credentials']

    URL = utils.decrypt_string(DECRIPTION_KEY, credentials['url'])
    USERNAME = utils.decrypt_string(DECRIPTION_KEY, credentials['username'])
    PASSWORD = utils.decrypt_string(DECRIPTION_KEY, credentials['password'])
    
    match optional[0]:
        case 1:
            #https://itelbposmartsolutions.sharepoint.com/sites/DataScienceHub/_api/Web/GetFolderById('9b04779c-cf8d-47b0-8862-bb20e367d99c')
            #https://itelbposmartsolutions.sharepoint.com/:f:/r/sites/DataScienceHub/Shared%20Documents/Human%20Resources/Coadvantage/Time%20Sheet%20Bucket?csf=1&web=1&e=EBQ7TP
            navigate_n_download(URL, USERNAME, PASSWORD, WEBPROFILE, WEBDRIVERPATH)

            print('Get file')
            local_filename = get_file(FILEFOLDER)[0]

            print('define sharepoint location')
            folder_id = get_folder_id(SHAREPOINT_FOLDER)

            print('create a sharepoint connection')
            sharepoint_cntn = sharepoint_wrapper.get_datascience_hub_ctx()

            print('upload file to sharepoint')
            sharepoint_wrapper.upload_file_to_sharepoint_folder(sharepoint_cntn, folder_id, local_filename, f"{FILEFOLDER}/{local_filename}")

            delete_file(FILEFOLDER, local_filename)

def get_folder_id(folder_key):

    folder_data = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]

    folder_id = folder_data['id']
    print(folder_id)

    return folder_id

def get_file(path: str):

    dir_list = os.listdir(path)
    csv_files = []

    for i in dir_list:
        if i.endswith('.csv') and i.startswith('CalculatedTimeByCalendarDay-HoursReportByDay'):
            csv_files.append(i)

    return csv_files

def delete_file(path: str, file_name):

    try:
        print('deleting file')
        file = path+'/'+file_name
        os.remove(f"{file}")
    except:
        print('Unable to delete file')



def navigate_n_download(url, username, password, webprofile, webdriverpath):

    first_webrowser_setup = seleniumutils.SeleniumUtils(webprofile, webdriverpath)
    first_webrowser_setup.setUp(url)

    first_webrowser_setup.findelement_xpath('//*[@id="FldUsername"]/input')
    first_webrowser_setup.sendkeys_to_element(username)
    print('user wrote')

    first_webrowser_setup.findelement_xpath('//*[@id="FldPasswordView"]/input')
    first_webrowser_setup.sendkeys_to_element(password)
    print('password wrote')

    first_webrowser_setup.findelement_xpath('//*[@id="loginPage"]/form/article/section[3]/div/div/fieldset/div[3]/button')
    first_webrowser_setup.click()
    print('logged in')

    sleep(2)

    first_webrowser_setup.findelement_xpath('//*[@id="mainMenuBtn"]')
    first_webrowser_setup.click()
    print('display menu')

    sleep(2)

    first_webrowser_setup.findelement_xpath('//*[@id="reports"]')
    first_webrowser_setup.click()
    print('see options in "my Reports"')

    sleep(2)

    first_webrowser_setup.findelement_xpath('//*[@id="reports"]/ul/li[2]')
    first_webrowser_setup.click()
    print('go to my saved reports')

    sleep(3)

    first_webrowser_setup.findelement_xpath('//*[@id="_feature"]/div/div[3]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[4]/div[3]/div[1]/div/ul/li/div/div/label/span[2]/input')
    first_webrowser_setup.click()
    print('click on other settings')

    sleep(2)

    first_webrowser_setup.findelement_xpath('//*[@id="_feature"]/div/div[3]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[82]/span')
    first_webrowser_setup.click()
    print('click on "Hours Report By Day"')

    sleep(20)

    first_webrowser_setup.findelement_xpath('//*[@id="_feature"]/div[2]/div[2]/div[2]/div/div/div[1]/div[4]/div[3]/div[1]')
    first_webrowser_setup.click()
    print('go to modify time entry section')

    sleep(2)

    first_webrowser_setup.findelement_name('calendarType')
    first_webrowser_setup.click()
    print('gdisplay daterange menu')

    sleep(1)

    first_webrowser_setup.findelement_xpath('//option[@value="40"]')
    first_webrowser_setup.click()
    print('go to modify time entry section')

    sleep(1)

    first_webrowser_setup.findelement_xpath('//input[@class="required"]')
    first_webrowser_setup.sendkeys_to_element(Keys.BACKSPACE)
    first_webrowser_setup.sendkeys_to_element('30')
    print('modify time period')

    sleep(1)

    first_webrowser_setup.findelement_xpath('//button[text()="Apply"]')
    first_webrowser_setup.click()
    print('apply time period to report')

    sleep(3)

    first_webrowser_setup.findelement_xpath('//*[@id="_feature"]/div[2]/div[2]/div[2]/div/div/div[1]/div[4]/div[3]/div[9]/div')
    first_webrowser_setup.click()
    print('click on options')

    sleep(1)

    first_webrowser_setup.findelement_xpath('//button[text()="Export..."]')
    first_webrowser_setup.click()
    print('click on Export')

    sleep(10)

    first_webrowser_setup.findelement_xpath('//button[text()="Export"]')
    first_webrowser_setup.click()
    print('Export file')

    sleep(5)

    first_webrowser_setup.tearDown()
    print('windows closed')


