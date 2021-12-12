# Skrumpen Email Client

![Alt  text](images/logo.png?raw=true)

## Introduction
The Skrumpen Email Client is an email client for recieving, viewing and sending mails. The application supports email-accounts from a variety of popular providers and works on most systems. The features supported by the application are the basic rudimentary email-functions such as reply/forward etc.

# Getting Started

## Prerequisites
These are the packages needed to run the application:
- Python
  - [Download](https://www.python.org/downloads/)
  - [Installation](https://www.tutorialspoint.com/how-to-install-python-in-windows)

- PySide2
  - [Installation guide](https://pypi.org/project/PySide2/)
  - When using Anaconda, use 
   ```
   conda install -c conda-forge pyside2
   ```

## Installation and Launching
To install the Skrumpen Email Client, download the repository from [here.](https://github.com/MartinBraas/emailclient)


Or clone into a folder with
```
git clone https://github.com/MartinBraas/emailclient
```

Once downloaded, navigate to the `emailclient/src` folder and enter
```
python main.py
```

## Usage
The Skrumpem Email Client allows users to acces their inboxes from popular email service providers such as Gmail or Outlook (see [Usage Issues](#usage-issues) for more info).

To get started with using the email client, enter your email address and password in the login-window after launching the application. After establishing a connection with the associated SMTP-server, the inbox-window will pop up and you will be able to use the full functionality of Skrumpen Email Client.

### Usage Issues
Running the program for the first time:
- When running the program for the first time, the load times after entering your login-credentials or when accessing folders in the drop-down menu, may be long and make the program inresponsive for a while. This is due to the `pycache` folder being created in the system files, and should only happen the first time the program is run.

Gmail-specific problems:
- For Gmail users, you need to allow 'acces from less secure apps', which can be read about [here](https://support.google.com/a/answer/6260879?hl=en)
- When logging in to the client for the first time, you might be prompted to enter a 'app-specific password'. Instructions on how to do so is found [here.](https://support.google.com/accounts/answer/185833?hl=en)

Problems for Anaconda users:
- Sometimes when installing PySide2, the current Anaconda enviroment has too many packages installed by default, which makes the enviroment solving take a very long time. To solve this, use `conda create -n foo -c conda-forge pyside2` to create a new Anaconda enviroment and install it there.

## Useful links

https://www.youtube.com/watch?v=mWZYn5I_jkY


## Install packages

`pip install -r requirements.txt`

## Testing

To run tests:
`pytest`
