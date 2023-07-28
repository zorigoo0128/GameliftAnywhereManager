import boto3
import json
import urllib.request
import string
import random
import logging

logging.basicConfig(
    filename='GameliftAnywhereManager.log', 
    level=logging.INFO,
    format='%(asctime)s:    %(name)s:   %(message)s')

class Gamelift_Anywhere:

    def __init__(self, fleet_id : str, location : str) -> None:
        self.gamelift_client = boto3.client('gamelift')
        self.fleet_id = fleet_id
        self.location = location
        logging.info('Gamelift Anywhere Init')


    def list(self) -> str:
        response = self.gamelift_client.list_compute(
            FleetId=self.fleet_id
        )
        logging.info('Gamelift Local Init')

        return response


    def create_game_session(self, session_name : str) -> str:
        response = self.gamelift_client.create_game_session(
            FleetId=self.fleet_id,
            MaximumPlayerSessionCount=16,
            Name=session_name,
            Location=self.location
        )
        return response['GameSession']
        
    def register(self, compute_name : str) -> bool:

        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

        response = self.gamelift_client.register_compute(
            FleetId=self.fleet_id,
            ComputeName=compute_name,
            IpAddress=external_ip,
            Location=self.location
        )
        return response
            

    def deregister(self, compute_name : str) -> bool:
        response = self.gamelift_client.deregister_compute(
            FleetId=self.fleet_id,
            ComputeName=compute_name,
        )
        
        return len(response) == 0
    
    
    def get_token(self, compute_name : str):
        response = self.gamelift_client.get_compute_auth_token(
            FleetId=self.fleet_id,
            ComputeName=compute_name,
        )
        

        if 'AuthToken' in response:
            return response['AuthToken']
        else:
            return ''

def generate_string(length : int = 1) -> str:
    return str(''.join(random.choices(string.ascii_uppercase + string.digits, k=length)))

class Gamelift_Manager:

    def __init__(self, fleet_id : str, location : str) -> None:
        self.fleet_id = fleet_id
        self.location = location
        self.Anywhere = Gamelift_Anywhere(fleet_id=self.fleet_id, location=self.location)
        logging.info('Gamelift Local Init')   


    def process(self, reset : bool = False) -> None:

        # Deregisters Currently Active Computes
        if reset:
            for compute in self.Anywhere.list()['ComputeList']:
                if 'ComputeName' in compute:
                    print(f'Deleting Compute: {compute["ComputeName"]}')
                    self.Anywhere.deregister(compute_name=compute['ComputeName'])
        

        # Registers New Compute
        new_compute_name = generate_string(length=12)
        
        register_result = self.Anywhere.register(compute_name=new_compute_name)
        sdk_endpoint = register_result['Compute']['GameLiftServiceSdkEndpoint']

        # Retrieves Auth Token
        token = self.Anywhere.get_token(compute_name=new_compute_name)



        return token, sdk_endpoint, new_compute_name
