# Gamelift Anywhere Manager

GameliftAnywhereManager is a Python script designed to manage game server instances on Amazon GameLift using the Gamelift Anywhere feature. It provides functionality to register and deregister compute instances, create game sessions, and retrieve authentication tokens for secure communication.


## Requirements

To use the GameliftAnywhereManager script, you'll need the following:

1. Python: Make sure you have Python installed on your system.
2. `boto3` The script uses the boto3 library to interact with Amazon GameLift. Install it using `pip`:


```
pip install boto3
```
3. `argparse`: This library is used to parse command-line arguments. If you don't have it already, install it:
```
pip install argparse
```


## How to Use
1.Clone the repository.

2.Open a terminal or command prompt, navigate to the folder where you saved the script, and run the following command:
```
python run.py -f <FLEET_ID> -l <LOCATION> [-r] <boolean>
```
Replace `<FLEET_ID>` with your Amazon GameLift fleet ID and `<LOCATION>` with the desired location where the game server instances should be placed. The `-r` flag is optional and used to reset and deregister any currently active compute instances before registering a new one


3. The script will output the authentication token, GameLift server SDK endpoint, and the compute name associated with the newly registered compute instance. It will also log this information in a file named `GameliftAnywhereManager.log.`

4. Use the provided server launch parameters to start your game server instances with the appropriate configuration.

## Script Arguments
The script can be executed with the following command-line arguments:

- `-f` or `--fleetid`: The Amazon GameLift fleet ID.
- `-l` or `--location`: The location where the game server instances should be placed.
- `-r` or `--reset`: Optional flag. If provided, any currently active compute instances will be deregistered before registering a new one.

## Logging
The script uses logging to record events and actions. The logs are saved in the `GameliftAnywhereManager.log` file in the same directory as the script.

