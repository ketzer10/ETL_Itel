import pysftp

def sftp(host, username, password, port):

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with pysftp.Connection(host=host, username=username, password=password, port=port, cnopts=cnopts) as sftp:
         with sftp.cd('/Employee Scheduling'):
            print(sftp.listdir('/Employee Scheduling'))


                