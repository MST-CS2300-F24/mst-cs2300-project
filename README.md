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
*Note: Your Powershell Execution Policy must be set to at least as permissive as remote-signed in order to run this properly on Windows.*

From here, install the necessary packages using the command `pip install -r requirments.txt`

Change the MySQL login information in `MySQL.py` and `initialize.py` to match your MySQL server.

## Initialization
- First, make sure your MySQL server is running.  
- To initialize the Database to your MySQL Server, run `inititialize.py` from your virtual environment.
- (Optional) You can run the `initialize.sql` file on your MySQl server in place of running the `initialize.py` file.  

## Deployment
To launch the web app, run `run.py` from your virtual environment.

## Use

1. **Login**: You initially begin logged in. If you press the `Logout` button, enter your credentials to access the system.  Default credentials are Username: `admin` and Password: `CS2300`
2. **Dashboard**: Click on the `Dashboard` tab to view key metrics and statistics.
3. **Manage Data**:
    - **Aircraft**: Navigate to the `Aircraft` tab to view, edit, or delete aircraft records.
    - **Airports**: Navigate to the `Airports` tab to view, edit, or delete airport records.
    - **Flights**: Navigate to the `Flights` tab to view, edit, or delete flight records.
    - **Maintenance Logs**: Navigate to the `Maintenance Logs` tab to view, edit, or delete maintenance log records.
    - **Maintenance Schedules**: Navigate to the `Maintenance Schedules` tab to view, edit, or delete maintenance schedule records.
4. **Add Data**: Navigate to the `Add` tab, then select an option from the left sidebar to add an entry in the respective table.
5. **Export Data**: Use the export buttons available on each data management page to download records as CSV files.
6. **Reports**: Generate performance reports for specific aircraft by clicking `View` on any aircraft in the `Aircraft` Tab.

**Have fun exploring the project!**
