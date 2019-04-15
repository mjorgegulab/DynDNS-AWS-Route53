#!/usr/bin/env python3

import boto3
import sys
from urllib.request import urlopen
from time import sleep


def check():
    global SERVICE_TYPE
    global KEY_ID
    global KEY_ACCESS
    global REGION

    if len(sys.argv) != 4:
        print("[!] Too few arguments.\n")
        sys.exit(0)
    else:
        SERVICE_TYPE = str(sys.argv[1])
        KEY_ID = str(sys.argv[2])
        KEY_ACCESS = str(sys.argv[3])
        REGION = 'us-east-1'


def init_service():
    global SERVICE_TYPE
    global KEY_ID
    global KEY_ACCESS
    global REGION
    global MY_IP

    try:
        client = boto3.client(SERVICE_TYPE,
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=KEY_ACCESS,
                              region_name=REGION)
        MY_IP = check_ip()
        return client
    except e:
        print("[!] Error!\n")
        print(e)
        sys.exit(0)


def check_ip():
    try:
        my_ip = urlopen('http://ip.42.pl/raw').read()
        return my_ip.decode("utf-8")
    except e:
        print("[!] Error getting ip.\n")


def set_dynamic_ip(client, ip):
    try:
        client.update_domain_entry(
            domainName='andsec.ch',
            domainEntry={
                'id': '106403181',
                'name': 'www.andsec.ch',
                'target': str(ip),
                'isAlias': False,
                'type': 'A'
            }
        )
    except:
        print("[!] Error modifying dns record.\n")


def main():
    global MY_IP

    check()
    api_client = init_service()
    MY_IP = '1.1.1.1'
    while True:
        if MY_IP != check_ip():
            MY_IP = check_ip()
            set_dynamic_ip(api_client, MY_IP)
        print(MY_IP)
        sleep(5)


if __name__ == '__main__':
        main()
