from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchAttributeException
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

class SeleniumUtils:

    '''
    This class was created to support automations for web navigation
    using selenium. It is necessary to define the following values in order
    to create the SeleniumUtils object:
        - webProfile: It is a string that refers to folder path wich contains all the
        navigation info of your chrome web browser. It is neccesary in order to
        avoid the login with 2FA that many web platforms requires when you sign in
        for the first time.
        - webdriverPath: To avoid install in every run the chrome webdriver it is
        necessary to define the path to use the executable of google chrome.
    '''

    def __init__(self, webProfile, webdriverPath):
        self.webProfile = webProfile
        self.webdriverPath = webdriverPath

    def setUp(self, url):
        '''
        Start the web browser element and load the required web platform.
        It needs:
            - url: string to web page.
        '''
        self.chrome_options = webdriver.ChromeOptions()
        my_chrome_options = self.chrome_options
        my_chrome_options.add_argument('disable-notifications')
        my_chrome_options.add_argument(f'user-data-dir={self.webProfile}')

        self.driver = webdriver.Chrome(self.webdriverPath, options=my_chrome_options)

        driver = self.driver

        driver.get(url)
        driver.maximize_window()

        sleep(2)

    def findelement_xpath(self, xpath):
        '''
        find and keep in memory an element from the DOM using its xpath
            - xpath: string.
        '''
        driver = self.driver
        self.element = driver.find_element('xpath', xpath)

    def findelement_name(self, name):
        '''
        find and keep in memory an element from the DOM using its html name
            - name: string.
        '''
        driver = self.driver
        self.element = driver.find_element('name', name)

    def sendkeys_to_element(self, keys):
        '''
        press a key in order to excecute a command or input data
        into any type of input elemnt from the DOM
            - keys: string or Key object from Selenium.Key class.
        '''
        element = self.element
        element.send_keys(keys)

    def click(self):
        '''
        Excecute click action.
        '''
        element = self.element
        element.click()
        
    def tearDown(self):
        '''
        Terminate the web driver element.
        '''
        sleep(5)
        self.driver.quit()

        


