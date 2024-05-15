### General

All commands should be run from the root directory of the project.

### Installing python

Run the following commands to install python3 if necessary,<br>

1. `sudo apt-get update` (enter your password if prompted)
2. `sudo apt-get python3.10`

Then check the python version is at least 3.10 by running,<br>

`python3 --version`

### Installing pip

If you do not have pip installed, run the following command,

`sudo apt install python3-pip`

Then check pip installation by running,

`python3 -m pip --version`

### Setup python virtual environment

To install virtual environments on linux,<br>

1. `python3 -m venv backend/venv`
2. `source backend/venv/bin/activate`
3. `pip install -r backend/requirements.txt`

### Install sqlite3

Run the following command to install sqlite3,

`sudo apt install sqlite3`

### Run the flask server

From the root of the project use command,<br>

`python3 -m flask run`

which will run a local development server on port 8080