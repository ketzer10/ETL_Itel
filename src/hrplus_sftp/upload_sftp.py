import pysftp
import os

from datetime import date, timedelta
from cryptography.fernet import Fernet

import utils.utils as utils

today = date.today()

if today.weekday() == 0:
    print(today.weekday())
    time_delta = timedelta(2)
    desire_date = str(today-time_delta)
    FINAL_DATE = desire_date.replace('-','')
    FINAL_DATE_2 = (str(today-timedelta(1))).replace('-','')


else:
    time_delta = timedelta(1)
    desire_date = str(today-time_delta)
    FINAL_DATE = desire_date.replace('-','')
    FINAL_DATE_2 = FINAL_DATE


desire_date = str(today-time_delta)
FINAL_DATE = desire_date.replace('-','')

PATH_F1 = f'./src/altice/data/PTD_Altice_{FINAL_DATE}_{FINAL_DATE_2}.csv'
PATH_F2 = f'./src/tds/data/PTD_TDS_{FINAL_DATE}_{FINAL_DATE_2}.csv'

file1 = open('./secrets/keys/public.key', 'rb')  # Open the file as wb to read bytes
DECRIPTION_KEY = file1.read()  # The key will be type bytes

def main(optional: list):

    print(optional)

    credentials = utils.get_credentials()['ptd_sftp_service']

    HOST = utils.decrypt_string(DECRIPTION_KEY, credentials['host'])
    USERNAME = utils.decrypt_string(DECRIPTION_KEY, credentials['username'])
    PASSWORD = utils.decrypt_string(DECRIPTION_KEY, credentials['password'])

    match optional[0]:

        case 1:
            print('Loading TDS PTD data to SFTP')

            try:
                sftp(host=HOST,username=USERNAME,password=PASSWORD,port=4011, path=PATH_F2)
                load_success = True
            except:
                print('something happens with SFTP service')
                load_success = False

            if load_success:
                if os.path.exists(PATH_F2):
                    os.remove(PATH_F2)
                else:
                    print("The file does not exist")
            else:
                print('File is not deleted due to issues with SFTP service')

        case 2:
            print('Loading Altice PTD data to SFTP')

            try:
                sftp(host=HOST,username=USERNAME,password=PASSWORD,port=4011, path=PATH_F1)
                load_success = True
            except:
                print('something happens with SFTP service')
                load_success = False

            if load_success:
                if os.path.exists(PATH_F1):
                    os.remove(PATH_F1)
                else:
                    print("The file does not exist")
            else:
                print('File is not deleted due to issues with SFTP service')
            

def sftp(host, username, password, port, path):

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with pysftp.Connection(host=host, username=username, password=password, port=port, cnopts=cnopts) as sftp:

         with sftp.cd('/Productive Time Data/Imported'):
            
            sftp.put(path)
            print(sftp.listdir('/Productive Time Data/Imported'))

