#!/usr/bin/env python3

import boto3
import sys
import datetime
from urllib.request import urlopen
from time import sleep
from cryptor import AESCipher


banner = '''  ___               ___  _  _ ___      ___      _____ 
 |   \ _  _ _ _ ___|   \| \| / __|___ /_\ \    / / __|
 | |) | || | ' \___| |) | .` \__ \___/ _ \ \/\/ /\__ \\
 |___/ \_, |_||_|  |___/|_|\_|___/  /_/ \_\_/\_/ |___/
       |__/                                           
'''

global KEY_ID
global KEY_ACCESS

KEY_ID = b'z3+XCgcbyXfzE6c9avvfKYPyaayAkQjzJ7uEuuMALy2EKeMMxjtttUMuOaDGQUcf'
KEY_ACCESS = b'l0Q4/U1hXtf1dknVhLXjvMgPdxNeQutYDv2Ta4e/yAPe59cTRB5nAkH38mgo7atpy3QEHP1d2Dqz8IDHjw4XNZhXMpyd8rqHDENyrrSzIgE='


def check():
    global REGION
    global ZONE_ID
    global FQDN
    global MY_IP

    if len(sys.argv) != 4:
        print("[!] Error on arguments.")
        print("Example: {} password zone_id fqdn".format(sys.argv[0]))
        sys.exit(0)
    else:
        ZONE_ID = str(sys.argv[2])
        FQDN = str(sys.argv[3])
        REGION = 'us-east-1'
        try:
            MY_IP = check_ip()
        except:
            pass


def init_service():
    global KEY_ID
    global KEY_ACCESS
    global REGION

    crypto = AESCipher(str(sys.argv[1]))

    try:
        client = boto3.client('route53',
                              aws_access_key_id=str(crypto.decrypt(KEY_ID)),
                              aws_secret_access_key=str(crypto.decrypt(KEY_ACCESS)),
                              region_name=REGION)
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
        print("[*] Record modified! " + str(datetime.datetime.now()) + "\n")
    except:
        print("[!] Error modifying dns record.")
        pass


def main():
    global MY_IP
    global ZONE_ID
    global FQDN

    check()
    print(banner + "\n")

    try:
        while True:
            if MY_IP != check_ip():
                api_client = init_service()
                MY_IP = check_ip()
                set_dynamic_ip(api_client, MY_IP, ZONE_ID, FQDN)
                del api_client
            print("Your IP is " + MY_IP + " at " + str(datetime.datetime.now()))
            sleep(120)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
	sys.exit(1)
        main()
