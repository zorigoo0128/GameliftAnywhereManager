import gamelift_anywhere 
import logging
import subprocess
import argparse
import os
import sys

logging.basicConfig(
    filename='GameliftAnywhereManager.log', 
    level=logging.INFO,
    format='%(asctime)s:    %(name)s:   %(message)s')


def main():

    try:
        parser = argparse.ArgumentParser(description="GameliftAnywhereManager")
        parser.add_argument('-f', '--fleetid', type=str, default=None, required=True)
        parser.add_argument('-l', '--location', type=str, default=None, required=True)
        parser.add_argument('-r', '--reset', type=bool, default=False, required=False)
        
        args, leftovers = parser.parse_known_args()

        if not args.fleetid or not args.location:
            print("Please enter following parameters: -l/--location and -f/--fleetid")
            return

        logging.info(f'Starting GameliftAnywhereManager with fleet id: {args.fleetid}, location: {args.location}')

        manager = gamelift_anywhere.Gamelift_Manager(fleet_id=args.fleetid, location=args.location)
        
        auth_token, sdk_endpoint, compute_name = manager.process(reset=args.reset)
        
        print(f'----\nFleetID: {args.fleetid} \nCompute Name: {compute_name} \nGameliftServerSdkEndpoint: {sdk_endpoint} \nAuth Token: {auth_token}\n-----\n')
        print(f'Server Launch Parameter: -fleetid={args.fleetid} -hostid={compute_name} -websocketurl={sdk_endpoint} -authtoken={auth_token}')
        logging.info(f'Server Launch Parameter: -fleetid={args.fleetid} -hostid={compute_name} -websocketurl={sdk_endpoint} -authtoken={auth_token}')  

    except KeyboardInterrupt:
        logging.info('Interrupted by keyboard...')  
        print("Exiting...")

        sys.exit(0)


    except Exception as e:
        logging.info('An error occurred:', e)  
        print("An error occurred:", e)

if __name__ == '__main__':
    main()