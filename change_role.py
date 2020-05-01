#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import logging
from argparse import ArgumentParser, REMAINDER
from util import get_url, post_and_wait, put_and_wait, delete, wait_on_tasks
import time
import csv


def update_device(ip, role):


    #print(json.dumps(payload,indent=2))
    #return
    print('Changing role of device IP {} to {}: '.format(ip, role), end='')
    response = get_url("dna/intent/api/v1/network-device/ip-address/{}".format(ip))
    try:
        deviceid = response['response']['id']
        oldrole = response['response']['role']
    except ValueError as e:
        print(e)
        return
    if oldrole == role:
        print("Oldrole {} same as newrole {}, skipping".format(oldrole, role))
        return
    payload = {
        "id": deviceid,
        "role": role,
        "roleSource": "MANUAL"
        }
    logging.debug(json.dumps(payload))
    response = put_and_wait("dna/intent/api/v1/network-device/brief", data=payload)
    task = response['id']
    time.sleep(2)
    tree = get_url("dna/intent/api/v1/task/{}/tree".format(task))
    logging.debug(json.dumps(tree,indent=2))

    for t in tree['response']:
        if 'failureReason' in t:
            print(t['failureReason'])
        else:
            #progress = json.loads(t['progress'])

            #print (" ".join(['{}:{}'.format(k, progress[k]) for k in progress.keys()]))
            print(t['progress'])


def change_ip(file):
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            params = dict(row)
            #print(json.dumps(params))
            update_device(params['ip'], params['role'])

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--rolefile', type=str, required=False,
                        help="mgmt file.  csv of managementIP, role")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()

    if args.v:

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("DEBUG ENABLED")

    if args.rolefile:
        change_ip(args.rolefile)