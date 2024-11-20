# flight-ops-db

## Prerequisites
- Python 3.11.7
- MySQL Enterprise 9.1.0

## Installation
After cloning the repository, navigate to it's directory.  
Run the following commands to create and activate your virtual environment:  
```
python -m venv .env
.env/Scripts/activate  
```

From here, install the necessary packages using the command `pip install -r requirments.txt`

Change the MySQL login information in `MySQL.py` and `initialize.py` to match your MySQL server.

## Initialization
To initialize the Database to your MySQL Server, run `inititialize.py` from your virtual environment.

## Deployment
To launch the web app, run `run.py` from your virtual environment.