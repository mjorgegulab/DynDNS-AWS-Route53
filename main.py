#!/usr/bin/env python3

import boto3
import sys
from urllib.request import urlopen
from time import sleep


def check():
    global KEY_ID
    global KEY_ACCESS
    global REGION
    global ZONE_ID
    global FQDN

    if len(sys.argv) != 5:
        print("[!] Error on arguments.")
        print("Example: {} key_id key_access_key zone_id fqdn".format(sys.argv[0]))
        sys.exit(0)
    else:
        KEY_ID = str(sys.argv[1])
        KEY_ACCESS = str(sys.argv[2])
        ZONE_ID = str(sys.argv[3])
        FQDN = str(sys.argv[4])
        REGION = 'us-east-1'


def init_service():
    global KEY_ID
    global KEY_ACCESS
    global REGION
    global MY_IP

    try:
        client = boto3.client('route53',
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=KEY_ACCESS,
                              region_name=REGION)
        MY_IP = check_ip()
        return client
    except:
        print("[!] Error contacting with aws API!")
        sys.exit(0)


def check_ip():
    try:
        my_ip = urlopen('http://ip.42.pl/raw').read()
        return my_ip.decode("utf-8")
    except:
        print("[!] Error getting ip.")


def set_dynamic_ip(client, ip, zone_id, fqdn):
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Comment': 'dyndns-script',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': fqdn,
                            'Type': 'A',
                            'TTL': 60,
                            'ResourceRecords': [
                                {
                                    'Value': ip
                                }
                            ]
                        }
                    }
                ]
            }
        )
        print("[*] Record modified!")
    except:
        print("[!] Error modifying dns record.")
        pass


def main():
    global MY_IP
    global ZONE_ID
    global FQDN

    check()
    api_client = init_service()
    
    while True:
        if MY_IP != check_ip():
            MY_IP = check_ip()
            set_dynamic_ip(api_client, MY_IP, ZONE_ID, FQDN)
        print(MY_IP)
        sleep(5)


if __name__ == '__main__':
        main()
