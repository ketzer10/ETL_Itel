# ETL Scripts itel Data Science and Innovation

## Description
Contains ETL scripts for various client systems, tools and technologies. It also contains an Office 365 wrapper used to access Sharepoint, Outlook, and Excel Online resources.

## Python version and dependencies
For this project Python 3.10.0 is used since it is the latest version at the writing of this README. It should be noted that Python 3.10.0 will not run on Windows 7 or earlier. Additionally, the use of the `venv` module for creating virtual environments is recommended since [it ships with Python 3.3+.](https://docs.python.org/3/library/venv.html) 

The dependencies for this project are stipulated in the `requirements.txt` document specifying the exact version of the dependency used. Because of this, contributors to this project are expected to properly add dependencies to the `requirements.txt` file. Furthermore, it is expected that the end user will use `pip` as the package management system.

## Private keys and secrets
The whole project depends upon the `keys` and `secrets` folders in the root directory. The `secrets` folder contains encrypted passwords, usernames, IP addresses and other configuration files used throughout the repository. The purpose of storing this information in the repository is so that changes in passwords, usernames or IPs can be easily propagated throughout the team without the need of modifying `.ini` files manually in each computer where the script might be used.

However, it is recognized that storing these configuration options in a repository (albeit private) is not ideal. Because of this, the configuration files are encrypted and can only be decrypted using the private keys stored in the `keys` folder. By design, all of the contents in the `keys` folder are ignored by VCS (git). This is done to avoid storing encrypted secrets and private keys on the server. 

This approach requires the end user to populate the `keys` folder with the appropriate private keys and names. The approach is not perfect since the the program will know both the secret and the private key at runtime. However, this allows the team to read the code for the whole organization without knowing the secrets if they were not given the private key. Controlling access to the private keys is crucial in this approach. 
